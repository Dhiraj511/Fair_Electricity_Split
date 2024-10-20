# init_db.py
from app import app, db, User


def init_db():
    with app.app_context():
        new_user = User(username='john_doe', email='john@example.com')
        db.session.add(new_user)
        db.session.commit()


if __name__ == '__main__':
    init_db()
