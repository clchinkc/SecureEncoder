import hashlib
from flask_sqlalchemy import SQLAlchemy
import functools

db = SQLAlchemy()

class MD5Hash(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255), unique=True, nullable=False)
    md5_hash = db.Column(db.String(32), unique=True, nullable=False)

    def __init__(self, text, md5_hash):
        self.text = text
        self.md5_hash = md5_hash

def md5_encode(text):
    hash_object = hashlib.md5(text.encode())
    hash_hex = hash_object.hexdigest()
    existing_hash = MD5Hash.query.filter_by(md5_hash=hash_hex).first()
    if not existing_hash:
        new_hash = MD5Hash(text, hash_hex)
        db.session.add(new_hash)
        db.session.commit()
    return hash_hex

@functools.lru_cache(maxsize=1)
def md5_decode(hash_hex):
    match = MD5Hash.query.filter_by(md5_hash=hash_hex).first()
    if match:
        return match.text
    return "No match found"

def populate_db(faker, num_entries=1000):
    for _ in range(num_entries):
        sentence = faker.sentence()
        md5_encode(sentence)
