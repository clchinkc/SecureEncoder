import hashlib
from flask_sqlalchemy import SQLAlchemy
import functools
from sqlalchemy.ext.declarative import DeclarativeMeta
from typing import cast
from faker import Faker


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


def md5_encode(text: str) -> str:
    hash_object = hashlib.md5(text.encode())
    hash_hex = hash_object.hexdigest()
    existing_hash = MD5Hash.query.filter_by(md5_hash=hash_hex).first()
    if not existing_hash:
        new_hash = MD5Hash(text, hash_hex)
        db.session.add(new_hash)
        db.session.commit()
    return hash_hex


@functools.lru_cache(maxsize=128)
def md5_decode(hash_hex: str) -> str:
    match = MD5Hash.query.filter_by(md5_hash=hash_hex).first()
    return match.text if match else "No match found"


def populate_db(faker: Faker, num_entries: int = 1000) -> None:
    for _ in range(num_entries):
        sentence = faker.sentence()
        md5_encode(sentence)
