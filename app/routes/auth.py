from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from ..extensions import db, limiter
from ..models.user import User

from argon2 import PasswordHasher 
from argon2.exceptions import VerifyMismatchError 

from urllib.parse import urlparse, urljoin 

def is_safe_url(target: str) -> bool:
    """
    Checks if the given URL is safe for redirection (i.e., same origin).
    This is a common security measure to prevent open redirect vulnerabilities.
    """
    if not target:
        return False 
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ("http", "https") and ref_url.netloc == test_url.netloc


ph = PasswordHasher()

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.get("/login")
def login_form():
    """
    Shows the login form.
    """
    if current_user.is_authenticated:
        return redirect(url_for("auth.dashboard"))
    return render_template("login.html")

@auth_bp.post("/login")
@limiter.limit("5 per minute")  # Rate limit to prevent brute-force attacks
def login_submit():
    """
    Handles login form submission.
    - Reads email and password
    - Verifies password hash (Argon2)
    - Logs in the user if valid
    - Redirects safely to ?next=... if provided
    """
    email = request.form.get("email", "").strip().lower()
    password = request.form.get("password", "")

    user = User.query.filter_by(email=email).first()
    if not user:
        flash("Invalid credentials.", "danger")
        return redirect(url_for("auth.login_form"))

    try:
        ok = ph.verify(user.password_hash, password)
    except VerifyMismatchError:
        ok = False

    if not ok:
        flash("Invalid credentials.", "danger")
        return redirect(url_for("auth.login_form"))

    login_user(user)
    flash("Login successful!", "success")

    # SAFE NEXT REDIRECT (buraya eklenecek demiştin)
    next_url = request.args.get("next")
    if next_url and is_safe_url(next_url):
        return redirect(next_url)

    return redirect(url_for("auth.dashboard"))

@auth_bp.get("/dashboard")
@login_required 
def dashboard():
    """
    A protected dashboard route that only logged-in users can access.
    """
    return render_template("dashboard.html")

@auth_bp.get("/logout")
@login_required
def logout():
    """
    Logs out the current user.
    """
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("auth.login_form"))

@auth_bp.get("/register")
def register_form():
    """
    Shows the registration form.
    """
    return render_template("register.html")

@auth_bp.post("/register")
def register_submit():
    print("DEBUG: register_submit HIT")
    """
    Handles registration form submission.
    - Reads input fields 
    - Validates them server_side 
    - Saves the user to the database
    """
    name = request.form.get ("name", "").strip()
    surname = request.form.get("surname", "").strip()
    tckn = request.form.get("tckn", "").strip()
    print("DEBUG TCKNN:", repr(tckn), "LEN:", len(tckn))
    phone = request.form.get("phone", "").strip()
    email = request.form.get("email", "").strip().lower()

    password = request.form.get("password", "")
    confirm_password = request.form.get("confirm_password", "")


    if len(password) < 8:
        flash("Password must be at least 8 characters.", "danger")
        return redirect(url_for("auth.register_form"))
    
    if password != confirm_password:
        flash("Passwords do not match.", "danger")
        return redirect(url_for("auth.register_form"))

    # --- Basic server-side validation (we will improve later.) ---
    if not name or not surname:
        flash("Name and surname are required.", "danger")
        return redirect(url_for("auth.register_form"))
    
    if not (tckn.isdigit() and len(tckn) == 11):
        flash("TCKN must be an exactly 11 digits.", "danger")
        return redirect(url_for("auth.register_form"))

    if "@" not in email:
        flash("Please enter a valid email.address.", "danger")
        return redirect(url_for("auth.register_form"))

    # Check duplicates
    if User.query.filter_by(email=email).first():
        flash("This email is already registered.", "warning")
        return redirect(url_for("auth.register_form"))   
    
    if User.query.filter_by(tckn=tckn).first():
        flash("This TCKN is already registered.", "warning")
        return redirect(url_for("auth.register_form"))
    
    # Save to DB
    user = User(
        name=name,
        surname=surname,
        tckn=tckn,
        phone=phone,
        email=email,
        password_hash=ph.hash(password),
    )    
    db.session.add(user)
    db.session.commit()

    flash("Registration successful!", "success")
    return redirect(url_for("auth.register_form")) 
