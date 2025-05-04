from __future__ import annotations
from ..database import db
from datetime import datetime, date
from typing import Optional

class Attendance(db.Model):
    __tablename__ = 'attendance'

    id: int = db.Column(db.Integer, primary_key=True)
    employee_id: int = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    date: date = db.Column(db.Date, nullable=False)
    time_in: datetime = db.Column(db.DateTime, nullable=False)
    time_out: Optional[datetime] = db.Column(db.DateTime)
    status: str = db.Column(db.String(20), default='present')

    employee = db.relationship('Employee', backref=db.backref('attendances', lazy=True))

    def __repr__(self):
        return f'<Attendance {self.employee.name} - {self.date}>'