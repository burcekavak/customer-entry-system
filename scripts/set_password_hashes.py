from app import create_app
from app.extensions import db
from app.models.user import User
from argon2 import PasswordHasher

ph = PasswordHasher()

def main():
    app = create_app()
    with app.app_context():
        users = User.query.filter(User.password_hash.is_(None)).all()
        print(f"Users to update: {len(users)}")

        for u in users:
            temp_password = "ChangeMe123!"
            u.password_hash = ph.hash(temp_password)

        db.session.commit()
        print("Done. All missing password_hash fields were filled.")

if __name__ == "__main__":
    main()