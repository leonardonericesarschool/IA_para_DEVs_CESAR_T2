from flask import Flask


def create_app():
    app = Flask(__name__)

    @app.after_request
    def set_security_headers(response):
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['Content-Security-Policy'] = "default-src 'none'"
        response.headers['X-XSS-Protection'] = '1; mode=block'
        return response

    from app.routes import bp
    app.register_blueprint(bp)

    return app
