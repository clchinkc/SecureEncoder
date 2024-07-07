from marshmallow import Schema, fields, validate


class SaveTextSchema(Schema):
    new_text = fields.String(required=True)


class ProcessTextSchema(Schema):
    text = fields.String(required=True, validate=validate.Length(min=1))
    operation = fields.String(
        required=True,
        validate=validate.OneOf(
            [
                "base64",
                "hex",
                "utf8",
                "latin1",
                "ascii",
                "url",
                "aes",
                "rsa",
                "md5",
                "huffman",
                "lz77",
                "lzw",
                "zstd",
                "deflate",
                "brotli",
            ]
        ),
    )
    action = fields.String(required=True, validate=validate.OneOf(["encode", "decode"]))


class UploadKeySchema(Schema):
    file = fields.Field(required=True)
