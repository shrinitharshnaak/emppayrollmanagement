from ..database import db
from datetime import datetime

class Leave(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    reason = db.Column(db.Text)
    status = db.Column(db.String(20), default='pending')  # pending, approved, rejected
    
    employee = db.relationship('Employee', backref=db.backref('leaves', lazy=True))

    def __repr__(self):
        return f'<Leave {self.employee.name} - {self.start_date}>'