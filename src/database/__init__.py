from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from typing import Any
import os

naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=naming_convention)
db = SQLAlchemy(metadata=metadata)

def init_app(app: Any) -> None:
    db.init_app(app)
    
    with app.app_context():
        # Import models to register them
        from ..models import Employee, Attendance, Leave, Payroll
        
        # Create all tables
        db.create_all()
        
        # Import and run seeder
        from .seeder import seed_admin
        seed_admin(db)
