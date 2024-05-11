from flask import Flask, request, jsonify, send_from_directory, make_response, session
from flask_cors import CORS
from werkzeug.utils import secure_filename
from werkzeug.exceptions import HTTPException
import os
from dotenv import load_dotenv
import logging
import json
from faker import Faker

from encoder_decoder import encode_base64, decode_base64, encode_hex, decode_hex, encode_utf8, decode_utf8, encode_latin1, decode_latin1, encode_ascii, decode_ascii, encode_url, decode_url
from encryption_decryption import ensure_aes_key, aes_encrypt, aes_decrypt, ensure_rsa_public_key, ensure_rsa_private_key, rsa_encrypt, rsa_decrypt
from md5_model import db, md5_encode, md5_decode, populate_db
from create_app import create_app

load_dotenv()

logging.basicConfig(level=logging.INFO)

app = create_app()
with app.app_context():
    db.create_all()  # Create database tables for our data models
    faker = Faker()
    populate_db(faker, 1000)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/api/upload_key', methods=['POST'])
def upload_key():
    file = request.files['file']
    if file.filename == '':
        logging.error("No file selected for upload")
        return jsonify({'error': 'No file selected'}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        return jsonify({'message': 'File uploaded successfully', 'filename': filename}), 200
    logging.error("Invalid file type")
    return jsonify({'error': 'Invalid file type'}), 400

@app.route('/api/files', methods=['GET'])
def list_files():
    files = [f for f in os.listdir(app.config['UPLOAD_FOLDER']) if os.path.isfile(os.path.join(app.config['UPLOAD_FOLDER'], f))]
    return jsonify(files)

@app.route('/api/download_key/<filename>')
def download_key(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(file_path):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)
    logging.error("File not found")
    return jsonify({'error': 'File not found'}), 404

@app.route('/api/save_text', methods=['POST'])
def save_text():
    """Store user input in session."""
    session['text'] = request.form.get('text', '')
    return jsonify(status="success")

@app.route('/api/process_text', methods=['POST'])
def process_text():
    data = request.get_json()
    session['text'] = data['text']
    session['operation'] = data['operation']
    session['action'] = data['action']

    operations = {
        'encode': {
            'base64': encode_base64,
            'hex': encode_hex,
            'utf8': encode_utf8,
            'latin1': encode_latin1,
            'ascii': encode_ascii,
            'url': encode_url,
            'aes': lambda x: aes_encrypt(x, ensure_aes_key(os.path.join(app.config['UPLOAD_FOLDER'], "aes_key.pem"))),
            'rsa': lambda x: rsa_encrypt(x, ensure_rsa_public_key(os.path.join(app.config['UPLOAD_FOLDER'], "rsa_public_key.pem"))),
            'md5': md5_encode,
        },
        'decode': {
            'base64': decode_base64,
            'hex': decode_hex,
            'utf8': decode_utf8,
            'latin1': decode_latin1,
            'ascii': decode_ascii,
            'url': decode_url,
            'aes': lambda x: aes_decrypt(x, ensure_aes_key(os.path.join(app.config['UPLOAD_FOLDER'], "aes_key.pem"))),
            'rsa': lambda x: rsa_decrypt(x, ensure_rsa_private_key(os.path.join(app.config['UPLOAD_FOLDER'], "rsa_private_key.pem"))),
            'md5': md5_decode,
        }
    }

    try:
        operation_func = operations[session['action']][session['operation']]
        result = operation_func(session['text'])
        session['result'] = result
        return jsonify({'result': result})
    except KeyError as e:
        logging.error(f"Operation or action not found: {e}")
        return jsonify({'error': 'Invalid operation or action'}), 400
    except Exception as e:
        logging.error(f"Error processing text: {e}")
        return jsonify({'error': str(e)}), 500

@app.after_request
def apply_security_headers(response):
    response.headers["Content-Security-Policy"] = "default-src 'self'; script-src 'self'; object-src 'none';"
    response.headers["X-Frame-Options"] = "SAMEORIGIN"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Referrer-Policy"] = "no-referrer"
    return response

@app.after_request
def add_session_to_response(response):
    response.set_cookie('files', json.dumps(session.get('files', [])))
    response.set_cookie('result', session.get('result', ''))
    response.set_cookie('operation', session.get('operation', ''))
    response.set_cookie('action', session.get('action', ''))
    response.set_cookie('text', session.get('text', ''))
    return response

@app.errorhandler(Exception)
def handle_exception(e):
    if isinstance(e, HTTPException):
        return e
    logging.error(f"Unhandled exception: {str(e)}")
    return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('FLASK_PORT', '5000')))
