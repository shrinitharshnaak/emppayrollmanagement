from __future__ import annotations
from ..database import db
from werkzeug.security import generate_password_hash, check_password_hash
from typing import Optional, List
from datetime import date

class Employee(db.Model):
    __tablename__ = 'employee'
    
    id: int = db.Column(db.Integer, primary_key=True)
    username: str = db.Column(db.String(80), unique=True, nullable=False)
    password_hash: str = db.Column(db.String(120), nullable=False)
    name: str = db.Column(db.String(100), nullable=False)
    email: str = db.Column(db.String(120), unique=True, nullable=False)
    position: Optional[str] = db.Column(db.String(80))
    salary: float = db.Column(db.Float, nullable=False)
    joining_date: date = db.Column(db.Date, nullable=False)
    role: str = db.Column(db.String(20), default='user')
    base_salary: float = db.Column(db.Float, nullable=False)
    hra: float = db.Column(db.Float, default=0.0)
    da: float = db.Column(db.Float, default=0.0)
    ta: float = db.Column(db.Float, default=0.0)
    pf: float = db.Column(db.Float, default=0.0)
    tax: float = db.Column(db.Float, default=0.0)

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    @property
    def is_admin(self) -> bool:
        return self.role == 'admin'

    @property
    def gross_salary(self) -> float:
        return self.base_salary + self.hra + self.da + self.ta
    
    @property
    def net_salary(self) -> float:
        return self.gross_salary - (self.pf + self.tax)

    def __repr__(self):
        return f'<Employee {self.username}>'