from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os

# Import your actual encoding and decoding functions
from encoder_decoder import encode_base64, decode_base64, encode_hex, decode_hex, encode_utf8, decode_utf8, encode_latin1, decode_latin1, encode_ascii, decode_ascii, encode_url, decode_url
from encryption_decryption import ensure_aes_key, aes_encrypt, aes_decrypt, ensure_rsa_public_key, ensure_rsa_private_key, rsa_encrypt, rsa_decrypt


app = Flask(__name__)
CORS(app)  # Enable CORS for all domains
app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'keys')
app.config['ALLOWED_EXTENSIONS'] = {'pem'}
app.secret_key = os.urandom(24)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/upload_key', methods=['POST'])
def upload_key():
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        return jsonify({'message': 'File uploaded successfully', 'filename': filename}), 200
    return jsonify({'error': 'Invalid file type'}), 400

@app.route('/process_text', methods=['POST'])
def process_text():
    data = request.get_json()
    text = data['text']
    operation = data['operation']
    action = data['action']

    try:
        result = "Operation not supported"
        if action == 'encode':
            if operation == 'base64':
                result = encode_base64(text)
            elif operation == 'hex':
                result = encode_hex(text)
            elif operation == 'utf8':
                result = encode_utf8(text).hex()
            elif operation == 'latin1':
                result = encode_latin1(text).hex()
            elif operation == 'ascii':
                result = encode_ascii(text)
            elif operation == 'url':
                result = encode_url(text)
            elif operation == 'aes':
                aes_key = ensure_aes_key(os.path.join(app.config['UPLOAD_FOLDER'], "aes_key.pem"))
                result = aes_encrypt(text, aes_key).hex()
            elif operation == 'rsa':
                public_key = ensure_rsa_public_key(os.path.join(app.config['UPLOAD_FOLDER'], "rsa_public_key.pem"))
                result = rsa_encrypt(text, public_key).hex()
            else:
                return jsonify({'error': 'Invalid operation'}), 400
        elif action == 'decode':
            if operation == 'base64':
                result = decode_base64(text)
            elif operation == 'hex':
                result = decode_hex(text)
            elif operation == 'utf8':
                result = decode_utf8(bytes.fromhex(text))
            elif operation == 'latin1':
                result = decode_latin1(bytes.fromhex(text))
            elif operation == 'ascii':
                result = decode_ascii(text)
            elif operation == 'url':
                result = decode_url(text)
            elif operation == 'aes':
                aes_key = ensure_aes_key(os.path.join(app.config['UPLOAD_FOLDER'], "aes_key.pem"))
                encrypted_bytes = bytes.fromhex(text)
                result = aes_decrypt(encrypted_bytes, aes_key).decode('utf-8')
            elif operation == 'rsa':
                private_key = ensure_rsa_private_key(os.path.join(app.config['UPLOAD_FOLDER'], "rsa_private_key.pem"))
                encrypted_bytes = bytes.fromhex(text)
                result = rsa_decrypt(encrypted_bytes, private_key)
            else:
                return jsonify({'error': 'Invalid operation'}), 400
        else:
            return jsonify({'error': 'Invalid action'}), 400
        return jsonify({'result': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/files', methods=['GET'])
def list_files():
    files = [f for f in os.listdir(app.config['UPLOAD_FOLDER']) if os.path.isfile(os.path.join(app.config['UPLOAD_FOLDER'], f))]
    return jsonify(files)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
