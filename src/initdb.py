import os
import sys

# Add the parent directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from src.app import create_app
from src.database import db

app = create_app()

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        print("Database initialized successfully!")