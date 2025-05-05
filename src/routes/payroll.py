from flask import Blueprint, render_template, request, redirect, url_for, flash
from ..models.payroll import Payroll
from ..models.employee import Employee
from ..routes.attendance import calculate_attendance_summary  # Import the function
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
        total_working_days, present_days, leave_days = calculate_attendance_summary(employee_id, month, year)
        payroll = Payroll(
            employee_id=employee_id,
            month=month,
            year=year,
            basic_salary=employee.salary,
            deductions=float(request.form.get('deductions', 0)),
            additions=float(request.form.get('additions', 0))
        )
        try:
            payroll.calculate_net_salary_dynamic(total_working_days, present_days, leave_days)
            db.session.add(payroll)
            db.session.commit()
        except ValueError as e:
            flash(str(e), 'danger')
            return redirect(url_for('payroll.calculate'))
        
        return redirect(url_for('payroll.report'))
        
    employees = Employee.query.all()
    return render_template('payroll/calculate.html', employees=employees)

@payroll_bp.route('/report')
def report():
    payrolls = Payroll.query.order_by(Payroll.year.desc(), Payroll.month.desc()).all()
    return render_template('payroll/report.html', payrolls=payrolls)