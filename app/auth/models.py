from datetime import datetime  # app/__init__.py
from app import db, bcrypt
from flask_login import UserMixin
from app import login_manager


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(20))
    user_email = db.Column(db.String(60), unique=True, index=True)
    user_password = db.Column(db.String(60))
    registration_date = db.Column(db.DateTime, default=datetime.now)

    # Class methods are belong to a class but are not associated with any class instance
    @classmethod
    def create_user(cls, user, email, password):

        user = cls(user_name=user,
                   user_email=email,
                   user_password=bcrypt.generate_password_hash(password).decode("utf-8")
                   )

        db.session.add(user)
        db.session.commit()
        return user


# This function returns the user id in unicode so must be wrapped in int() method
@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

