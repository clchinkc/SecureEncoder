import hashlib
from flask_sqlalchemy import SQLAlchemy
import functools
from sqlalchemy.ext.declarative import DeclarativeMeta
from typing import cast
from faker import Faker
from sqlalchemy.exc import SQLAlchemyError
import json
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field

db = SQLAlchemy()
BaseModel = cast(DeclarativeMeta, db.Model)


class MD5Hash(BaseModel):
    __tablename__ = "md5_hash"
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255), unique=True, nullable=False)
    md5_hash = db.Column(db.String(32), unique=True, nullable=False)

    def __init__(self, text: str, md5_hash: str) -> None:
        self.text = text
        self.md5_hash = md5_hash


class MD5HashSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = MD5Hash
        include_relationships = True
        load_instance = True
        sqla_session = db.session

    id = auto_field()
    text = auto_field()
    md5_hash = auto_field()


md5_hash_schema = MD5HashSchema()


def md5_encode(text: str) -> str:
    hash_object = hashlib.md5(text.encode())
    hash_hex = hash_object.hexdigest()
    existing_hash = MD5Hash.query.filter_by(md5_hash=hash_hex).first()
    if not existing_hash:
        new_hash = MD5Hash(text=text, md5_hash=hash_hex)
        db.session.add(new_hash)
        db.session.commit()
        return md5_hash_schema.dump(new_hash)["md5_hash"]
    return md5_hash_schema.dump(existing_hash)["md5_hash"]


@functools.lru_cache(maxsize=128)
def md5_decode(hash_hex: str) -> str:
    match = MD5Hash.query.filter_by(md5_hash=hash_hex).first()
    if match:
        return md5_hash_schema.dump(match)["text"]
    return "No match found"


def populate_db(faker: Faker, num_entries: int = 1000) -> None:
    db.session.autocommit = (
        False  # Assuming your SQL Alchemy settings allow control over autocommit
    )
    try:
        for i in range(num_entries):
            sentence = faker.sentence()
            md5_encode(sentence)
            if i % 100 == 0:
                db.session.flush()  # Flush the changes without committing them
        db.session.commit()  # Commit at the end of the operation
    except SQLAlchemyError as e:
        db.session.rollback()
        raise e
    finally:
        db.session.autocommit = True  # Restore autocommit settings
