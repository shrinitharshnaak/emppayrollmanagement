from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.engine import Engine
from sqlalchemy.orm import DeclarativeMeta
from typing import Any
import os

naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata: MetaData = MetaData(naming_convention=naming_convention)
db: SQLAlchemy = SQLAlchemy(metadata=metadata)

class BaseModel(db.Model):  # type: ignore
    __abstract__ = True
    
    def save(self) -> None:
        db.session.add(self)
        db.session.commit()
    
    def delete(self) -> None:
        db.session.delete(self)
        db.session.commit()
    
    @classmethod
    def get_by_id(cls, id: int) -> Any:
        return cls.query.get(id)

def init_app(app: Any) -> None:
    db.init_app(app)
    
    # Ensure instance folder exists
    if not os.path.exists(app.instance_path):
        os.makedirs(app.instance_path)
    
    with app.app_context():
        # Import models to register them
        from .models import Employee, Attendance, Leave, Payroll
        
        # Create all tables
        db.create_all()
        
        # Import and run seeder after tables are created
        from .database.seeder import seed_admin
        seed_admin(db)

from .database import db, init_app

__all__ = ['db', 'init_app']