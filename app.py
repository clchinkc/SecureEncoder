from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os

# Import your actual encoding and decoding functions
from encoder_decoder import encode_base64, encode_hex, decode_base64, decode_hex

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
            # Add other encoding operations here
        elif action == 'decode':
            if operation == 'base64':
                result = decode_base64(text)
            elif operation == 'hex':
                result = decode_hex(text)
            # Add other decoding operations here
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
