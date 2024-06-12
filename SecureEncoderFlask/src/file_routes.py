from flask import Blueprint, request, jsonify, send_from_directory, current_app
from werkzeug.utils import secure_filename
import os

file_bp = Blueprint('file_bp', __name__)

def allowed_file(filename, allowed_extensions):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

@file_bp.route('/api/upload_key', methods=['POST'])
def upload_key():
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    if file and allowed_file(file.filename, current_app.config['ALLOWED_EXTENSIONS']):
        filename = secure_filename(file.filename)
        file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
        return jsonify({'message': 'File uploaded successfully', 'filename': filename}), 201
    return jsonify({'error': "Invalid file type, a '.pem' file is needed"}), 400

@file_bp.route('/api/files', methods=['GET'])
def list_files():
    files = [f for f in os.listdir(current_app.config['UPLOAD_FOLDER']) if os.path.isfile(os.path.join(current_app.config['UPLOAD_FOLDER'], f))]
    return jsonify(files), 200

@file_bp.route('/api/download_key/<string:filename>')
def download_key(filename):
    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    if not os.path.exists(file_path):
        return jsonify({'error': 'Key not found'}), 404
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

@file_bp.route('/api/delete_key/<string:filename>', methods=['DELETE'])
def delete_key(filename):
    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], secure_filename(filename))
    if os.path.exists(file_path):
        os.remove(file_path)
        return jsonify({'message': 'File deleted successfully'}), 204
    else:
        return jsonify({'error': 'File not found'}), 404
