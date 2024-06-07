from flask import request, jsonify, send_from_directory, session
from werkzeug.utils import secure_filename
from werkzeug.exceptions import HTTPException
import os

import json
from faker import Faker

from .encoder_decoder import encode_base64, decode_base64, encode_hex, decode_hex, encode_utf8, decode_utf8, encode_latin1, decode_latin1, encode_ascii, decode_ascii, encode_url, decode_url
from .encryption_decryption import ensure_aes_key, aes_encrypt, aes_decrypt, ensure_rsa_public_key, ensure_rsa_private_key, rsa_encrypt, rsa_decrypt
from .md5_model import db, md5_encode, md5_decode, populate_db
from .compression_decompression import  lz77_compress, lz77_decompress, lzw_compress, lzw_decompress, zstd_compress, zstd_decompress, deflate_compress, deflate_decompress, brotli_compress, brotli_decompress
from .create_app import create_app, setup_logger
from .huffman import huffman_compress, huffman_decompress


app = create_app()
with app.app_context():
    db.create_all()
    faker = Faker()
    populate_db(faker, 10)

setup_logger(app)

@app.route('/')
def index():
    app.logger.debug('This is a debug message, visible only in development')
    app.logger.warning('This warning is logged in production')
    return "Hello, please check your log configuration based on the environment."

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/api/upload_key', methods=['POST'])
def upload_key():
    file = request.files['file']
    if file.filename == '':
        app.logger.error("No file selected for upload")
        return jsonify({'error': 'No file selected'}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return jsonify({'message': 'File uploaded successfully', 'filename': filename}), 201
    app.logger.error("Invalid file type, a '.pem' file is needed")
    return jsonify({'error': "Invalid file type, a '.pem' file is needed"}), 400

@app.route('/api/files', methods=['GET'])
def list_files():
    files = [f for f in os.listdir(app.config['UPLOAD_FOLDER']) if os.path.isfile(os.path.join(app.config['UPLOAD_FOLDER'], f))]
    return jsonify(files), 200

@app.route('/api/download_key/<filename>')
def download_key(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if not os.path.exists(file_path):
        app.logger.error("File not found")
        return jsonify({'error': 'Key not found'}), 404
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

@app.route('/api/delete_key/<filename>', methods=['DELETE'])
def delete_key(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(filename))
    if os.path.exists(file_path):
        os.remove(file_path)
        return jsonify({'message': 'File deleted successfully'}), 204
    else:
        return jsonify({'error': 'File not found'}), 404

@app.route('/api/save_text', methods=['PATCH'])
def save_text():
    data = request.get_json()
    current_text = session.get('text', None)
    new_text = data.get('new_text', None)

    if current_text is None and new_text is None:
        return jsonify({'message': 'No text provided'}), 204
    elif current_text is None and new_text is not None:
        session['text'] = new_text
        return jsonify({'message': 'Text created successfully', 'text': new_text}), 201
    elif current_text is not None and new_text is None:
        return jsonify({'message': 'No new text provided, text remains unchanged', 'text': current_text}), 304
    else:
        session['text'] = new_text
        return jsonify({'message': 'Text updated successfully', 'new_text': new_text}), 200

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
            'huffman': huffman_compress,
            'lz77': lz77_compress,
            'lzw': lzw_compress,
            'zstd': zstd_compress,
            'deflate': deflate_compress,
            'brotli': brotli_compress,
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
            'huffman': huffman_decompress,
            'lz77': lz77_decompress,
            'lzw': lzw_decompress,
            'zstd': zstd_decompress,
            'deflate': deflate_decompress,
            'brotli': brotli_decompress,
        }
    }

    try:
        operation_func = operations[session['action']][session['operation']]
        result = operation_func(session['text'])
        return jsonify({'result': result}), 200
    except KeyError as e:
        app.logger.error(f"Operation or action not found: {e}")
        return jsonify({'error': 'Invalid operation or action'}), 400
    except Exception as e:
        app.logger.error(f"Error processing text: {e}")
        return jsonify({'error': str(e)}), 500

@app.after_request
def apply_security_headers(response):
    response.headers['Strict-Transport-Security'] = 'max-age=63072000; includeSubDomains'
    response.headers["Content-Security-Policy"] = "default-src 'self'; script-src 'self'; object-src 'none';"
    response.headers["X-Frame-Options"] = "SAMEORIGIN"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Referrer-Policy"] = "no-referrer-when-downgrade"
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
    app.logger.error(f"Unhandled exception: {str(e)}")
    return jsonify({'error': str(e)}), 500 if isinstance(e, KeyError) or isinstance(e, ValueError) else 400

def main():
    app.run(host='0.0.0.0', port=int(app.config['FLASK_PORT']), debug=app.config['FLASK_DEBUG'], use_reloader=True, threaded=True)
