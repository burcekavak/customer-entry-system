import os 
try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass


class Config:
    """
    Project Configuration.
    
    We start with SQLite (no installation needed).
    Later we can switch to PostgreSQL for production readiness.
    """
    ENV = os.getenv("FLASK_ENV", "development")

    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-change-me")

    SQLALCHEMY_DATABASE_URI = "sqlite:///dev.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    SESSION_COOKIE_SECURE = (ENV == "production") 

    REMEMBER_COOKIE_HTTPONLY = True 
    REMEMBER_COOKIE_SAMESITE = "Lax"
    REMEMBER_COOKIE_SECURE = (ENV == "production")  

    RATELIMIT_STORAGE_URI = "memory://"