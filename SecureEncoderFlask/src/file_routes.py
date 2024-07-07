import os
from flask import Blueprint, request, jsonify, send_from_directory, current_app
from werkzeug.utils import secure_filename
from marshmallow import ValidationError
from .log_execution import log_execution
from .schemas import UploadKeySchema

file_bp = Blueprint("file_bp", __name__)


def allowed_file(filename: str, allowed_extensions: set[str]) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in allowed_extensions


@file_bp.route("/api/upload_key", methods=["POST"])
@log_execution
def upload_key():
    file_input = request.files.get("file")
    if not file_input:
        return jsonify({"error": "No file part"}), 400
    try:
        file = UploadKeySchema().load({"file": file_input})
    except ValidationError as err:
        return jsonify(err.messages), 400
    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400
    if file and allowed_file(
        file.filename, set(current_app.config["ALLOWED_EXTENSIONS"])
    ):
        filename = secure_filename(file.filename)
        file.save(os.path.join(current_app.config["UPLOAD_FOLDER"], filename))
        return jsonify(
            {"message": "File uploaded successfully", "filename": filename}
        ), 201
    return jsonify({"error": "Invalid file type, a '.pem' file is needed"}), 400


@file_bp.route("/api/files", methods=["GET"])
@log_execution
def list_files() -> tuple[jsonify, int]:
    files = [
        f
        for f in os.listdir(current_app.config["UPLOAD_FOLDER"])
        if os.path.isfile(os.path.join(current_app.config["UPLOAD_FOLDER"], f))
    ]
    return jsonify(files), 200


@file_bp.route("/api/download_key/<string:filename>")
@log_execution
def download_key(filename: str) -> jsonify:
    safe_filename = secure_filename(filename)
    upload_folder = current_app.config["UPLOAD_FOLDER"]
    file_path = os.path.join(upload_folder, safe_filename)
    fullpath = os.path.normpath(file_path)
    if not fullpath.startswith(os.path.normpath(upload_folder)):
        return jsonify({"error": "Invalid file path"}), 400
    if not os.path.exists(file_path):
        return jsonify({"error": "Key not found"}), 404
    return send_from_directory(
        current_app.config["UPLOAD_FOLDER"], safe_filename, as_attachment=True
    )


@file_bp.route("/api/delete_key/<string:filename>", methods=["DELETE"])
@log_execution
def delete_key(filename: str) -> jsonify:
    file_path = os.path.join(
        current_app.config["UPLOAD_FOLDER"], secure_filename(filename)
    )
    if os.path.exists(file_path):
        os.remove(file_path)
        return jsonify({"message": "File deleted successfully"}), 204
    else:
        return jsonify({"error": "File not found"}), 404
