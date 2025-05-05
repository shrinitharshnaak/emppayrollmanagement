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

    def calculate_net_salary(self, total_working_days, leave_days):
        daily_salary = self.basic_salary / total_working_days
        leave_deduction = daily_salary * leave_days
        self.net_salary = self.basic_salary + self.additions - (self.deductions + leave_deduction)
        return self.net_salary

    def calculate_net_salary_dynamic(self, total_working_days, present_days, leave_days):
        if total_working_days == 0:
            raise ValueError("Total working days cannot be zero.")
        
        daily_salary = self.basic_salary / total_working_days
        leave_deduction = daily_salary * leave_days
        earned_salary = daily_salary * present_days
        self.net_salary = earned_salary + self.additions - (self.deductions + leave_deduction)
        return self.net_salary