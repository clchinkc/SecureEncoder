from flask import Flask, jsonify, Response, session
from .create_app import create_app
from .md5_model import db, populate_db
from faker import Faker
from werkzeug.exceptions import HTTPException
import json

app: Flask = create_app()
with app.app_context():
    db.create_all()
    faker: Faker = Faker()
    populate_db(faker, 100)


# When serving a single-page application, we need to catch all routes and serve the index.html file.
@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def catch_all(path):
    return app.send_static_file("index.html")


@app.after_request
def apply_security_headers(response: Response):
    response.headers["Strict-Transport-Security"] = (
        "max-age=63072000; includeSubDomains"
    )
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; script-src 'self'; object-src 'none';"
    )
    response.headers["X-Frame-Options"] = "SAMEORIGIN"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Referrer-Policy"] = "no-referrer-when-downgrade"
    return response


@app.after_request
def add_session_to_response(response: Response):
    response.set_cookie("files", json.dumps(session.get("files", [])))
    response.set_cookie("result", session.get("result", ""))
    response.set_cookie("operation", session.get("operation", ""))
    response.set_cookie("action", session.get("action", ""))
    response.set_cookie("text", session.get("text", ""))
    return response


@app.errorhandler(Exception)
def handle_exception(e: Exception) -> Response:
    if isinstance(e, HTTPException):
        return jsonify({"error": e.description}), e.code
    app.logger.error(f"Unhandled exception: {str(e)}")
    return jsonify({"error": str(e)}), 500 if isinstance(e, KeyError) or isinstance(
        e, ValueError
    ) else 400


@app.errorhandler(404)
def page_not_found(e: HTTPException):
    return """<h1>404</h1><h2>The resource could not be found.</h2>""", 404


def main():
    if app.config["FLASK_DEVELOPMENT"]:
        app.run(
            port=int(app.config["FLASK_PORT"]),
            debug=app.config["FLASK_DEBUG"],
            use_reloader=True,
            threaded=True,
        )
    else:
        from waitress import serve

        serve(
            app=app,
            port=int(app.config["FLASK_PORT"]),
            url_scheme="https",
        )
