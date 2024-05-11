from src.md5_model import db, MD5Hash, md5_encode, md5_decode
from src.create_app import create_app
import pytest

@pytest.fixture
def app():
    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'WTF_CSRF_ENABLED': False  # Disable CSRF tokens in the form for testing purposes.
    })

    with app.app_context():
        db.create_all()

    return app

@pytest.fixture
def client(app):
    return app.test_client()

def test_md5_encode(app):
    # Use app context here for database operations
    with app.app_context():
        text = "hello world"
        encoded = md5_encode(text)
        stored_hash = MD5Hash.query.first()
        assert stored_hash.md5_hash == encoded  # Ensure it's correctly stored in DB
        assert len(encoded) == 32  # MD5 hashes should be 32 characters long

def test_md5_decode(app):
    with app.app_context():
        text = "hello world"
        encoded = md5_encode(text)
        decoded = md5_decode(encoded)
        assert decoded == text  # Ensure the decoded text matches the original

def test_md5_decode_no_match(app):
    with app.app_context():
        decoded = md5_decode("nonexistenthash")
        assert decoded == "No match found"  # Ensure correct message is returned when no match is found
