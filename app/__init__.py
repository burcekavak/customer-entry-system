from flask_wtf.csrf import CSRFProtect
from flask import Flask, render_template
from .config import Config
from .extensions import db, migrate, login_manager, limiter
from .models.user import User
from .routes.auth import auth_bp


def create_app():
    print("DEBUG: create_app started")

    app = Flask(__name__)
    app.config.from_object(Config)

    # CSRF protection
    csrf = CSRFProtect()
    csrf.init_app(app)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    limiter.init_app(app)

    # Register blueprints
    app.register_blueprint(auth_bp)

    # Security headers
    @app.after_request
    def add_security_headers(response):
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; "
            "style-src 'self' 'unsafe-inline'; "
            "script-src 'self'; "
            "img-src 'self' data:; "
            "form-action 'self'; "
            "frame-ancestors 'none'"
        )
        return response

    @app.get("/")
    def home():
        return render_template("home.html")

    @login_manager.user_loader
    def load_user(user_id: str):
        return db.session.get(User, int(user_id))

    return app