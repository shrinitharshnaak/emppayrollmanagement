from flask import Blueprint, render_template, request, redirect, url_for, flash
from ..models.payroll import Payroll
from ..models.employee import Employee
from ..database import db
from datetime import datetime

payroll_bp = Blueprint('payroll', __name__, url_prefix='/payroll')

@payroll_bp.route('/calculate', methods=['GET', 'POST'])
def calculate():
    if request.method == 'POST':
        employee_id = request.form['employee_id']
        month = int(request.form['month'])
        year = int(request.form['year'])
        
        employee = Employee.query.get_or_404(employee_id)
        payroll = Payroll(
            employee_id=employee_id,
            month=month,
            year=year,
            basic_salary=employee.salary,
            deductions=float(request.form.get('deductions', 0)),
            additions=float(request.form.get('additions', 0))
        )
        payroll.calculate_net_salary()
        db.session.add(payroll)
        db.session.commit()
        
        return redirect(url_for('payroll.report'))
        
    employees = Employee.query.all()
    return render_template('payroll/calculate.html', employees=employees)

@payroll_bp.route('/report')
def report():
    payrolls = Payroll.query.order_by(Payroll.year.desc(), Payroll.month.desc()).all()
    return render_template('payroll/report.html', payrolls=payrolls)