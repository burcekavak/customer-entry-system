from datetime import datetime
from ..extensions import db 
from flask_login import UserMixin

class User(UserMixin, db.Model):
    """
    Databse model for registered useres.

    NOTE:
    - For v1, we store TCKN as plain text to keep it simple.
    - In the next security phase, we will store it as HMAC/encrypted.
    """

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(50), nullable=False)
    surname = db.Column(db.String(50), nullable=False)

    tckn = db.Column(db.String(11), unique=True, nullable=False)

    phone = db.Column(db.String(20), nullable=False)

    email = db.Column(db.String(120), unique=True, nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False) 

    password_hash = db.Column(db.String(225), nullable=False) 