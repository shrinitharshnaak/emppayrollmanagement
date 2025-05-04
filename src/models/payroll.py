from ..database import db
from datetime import datetime

class Payroll(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    month = db.Column(db.Integer, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    basic_salary = db.Column(db.Float, nullable=False)
    deductions = db.Column(db.Float, default=0.0)
    additions = db.Column(db.Float, default=0.0)
    net_salary = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, processed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    employee = db.relationship('Employee', backref=db.backref('payrolls', lazy=True))

    def calculate_net_salary(self):
        self.net_salary = self.basic_salary + self.additions - self.deductions
        return self.net_salary