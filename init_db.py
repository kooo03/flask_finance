# init_db.py
from app import app, db

if __name__ == '__main__':
    with app.app_context():
        print(" Initializing database tables...")
        db.create_all()
        print("✅ Database tables created.")
