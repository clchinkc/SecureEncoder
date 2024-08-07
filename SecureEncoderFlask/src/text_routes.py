import os
from flask import Blueprint, request, jsonify, session, current_app
from marshmallow import ValidationError
from .schemas import SaveTextSchema, ProcessTextSchema

from .encoder_decoder import (
    encode_base64,
    decode_base64,
    encode_hex,
    decode_hex,
    encode_utf8,
    decode_utf8,
    encode_latin1,
    decode_latin1,
    encode_ascii,
    decode_ascii,
    encode_url,
    decode_url,
)
from .encryption_decryption import (
    ensure_aes_key,
    aes_encrypt,
    aes_decrypt,
    ensure_rsa_public_key,
    ensure_rsa_private_key,
    rsa_encrypt,
    rsa_decrypt,
)
from .md5_model import md5_encode, md5_decode
from .compression_decompression import (
    lz77_compress,
    lz77_decompress,
    lzw_compress,
    lzw_decompress,
    zstd_compress,
    zstd_decompress,
    deflate_compress,
    deflate_decompress,
    brotli_compress,
    brotli_decompress,
)
from .huffman import huffman_compress, huffman_decompress
from .log_execution import log_execution

text_bp = Blueprint("text_bp", __name__)


@text_bp.route("/api/save_text", methods=["PATCH"])
@log_execution
def save_text() -> tuple[jsonify, int]:
    try:
        data = SaveTextSchema().load(request.get_json())
    except ValidationError as err:
        return jsonify(err.messages), 400

    current_text = session.get("text", None)
    new_text = data.get("new_text", None)
    force_update = request.args.get("force_update", "false") == "true"

    if current_text is None and new_text is None:
        return jsonify({"message": "No text provided"}), 204
    elif current_text is None and new_text is not None:
        session["text"] = new_text
        return jsonify({"message": "Text created successfully", "text": new_text}), 201
    elif current_text is not None and new_text is None:
        return jsonify(
            {
                "message": "No new text provided, text remains unchanged",
                "text": current_text,
            }
        ), 304
    elif force_update:
        session["text"] = new_text
        return jsonify(
            {"message": "Text updated successfully", "new_text": new_text}
        ), 200
    else:
        return jsonify(
            {"message": "Text already exists, use force_update to overwrite"}
        ), 409


@text_bp.route("/api/process_text", methods=["POST"])
@log_execution
def process_text() -> jsonify:
    try:
        data = ProcessTextSchema().load(request.get_json())
    except ValidationError as err:
        return jsonify(err.messages), 400

    session["text"] = data["text"]
    session["operation"] = data["operation"]
    session["action"] = data["action"]

    operations = {
        "encode": {
            "base64": encode_base64,
            "hex": encode_hex,
            "utf8": encode_utf8,
            "latin1": encode_latin1,
            "ascii": encode_ascii,
            "url": encode_url,
            "aes": lambda x: aes_encrypt(
                x,
                ensure_aes_key(
                    os.path.join(current_app.config["UPLOAD_FOLDER"], "aes_key.pem")
                ),
            ),
            "rsa": lambda x: rsa_encrypt(
                x,
                ensure_rsa_public_key(
                    os.path.join(
                        current_app.config["UPLOAD_FOLDER"], "rsa_public_key.pem"
                    )
                ),
            ),
            "md5": md5_encode,
            "huffman": huffman_compress,
            "lz77": lz77_compress,
            "lzw": lzw_compress,
            "zstd": zstd_compress,
            "deflate": deflate_compress,
            "brotli": brotli_compress,
        },
        "decode": {
            "base64": decode_base64,
            "hex": decode_hex,
            "utf8": decode_utf8,
            "latin1": decode_latin1,
            "ascii": decode_ascii,
            "url": decode_url,
            "aes": lambda x: aes_decrypt(
                x,
                ensure_aes_key(
                    os.path.join(current_app.config["UPLOAD_FOLDER"], "aes_key.pem")
                ),
            ),
            "rsa": lambda x: rsa_decrypt(
                x,
                ensure_rsa_private_key(
                    os.path.join(
                        current_app.config["UPLOAD_FOLDER"], "rsa_private_key.pem"
                    )
                ),
            ),
            "md5": md5_decode,
            "huffman": huffman_decompress,
            "lz77": lz77_decompress,
            "lzw": lzw_decompress,
            "zstd": zstd_decompress,
            "deflate": deflate_decompress,
            "brotli": brotli_decompress,
        },
    }

    try:
        operation_func = operations[session["action"]][session["operation"]]
        result = operation_func(session["text"])
        return jsonify({"result": result}), 200
    except KeyError:
        return jsonify({"error": "Invalid operation or action provided"}), 400
    except Exception:
        return jsonify({"error": "An error occurred while processing the text"}), 500
