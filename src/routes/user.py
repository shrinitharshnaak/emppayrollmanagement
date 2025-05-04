from flask import Blueprint, render_template, session
from ..models.employee import Employee
from ..models.attendance import Attendance
from ..models.leave import Leave
from ..models.payroll import Payroll
from ..routes.auth import login_required
from datetime import datetime, date
from calendar import monthrange

user_bp = Blueprint('user', __name__, url_prefix='/user')

@user_bp.route('/dashboard')
@login_required
def dashboard():
    employee = Employee.query.get(session['user_id'])
    today = date.today()
    
    # Get attendance stats
    month_attendance = Attendance.query.filter_by(
        employee_id=employee.id,
        status='present'
    ).filter(
        Attendance.date.between(
            date(today.year, today.month, 1),
            today
        )
    ).count()
    
    # Get leave balance
    total_leaves = Leave.query.filter_by(
        employee_id=employee.id,
        status='approved'
    ).filter(
        Leave.start_date.between(
            date(today.year, 1, 1),
            today
        )
    ).count()
    
    # Get latest payslip
    latest_payroll = Payroll.query.filter_by(
        employee_id=employee.id
    ).order_by(Payroll.created_at.desc()).first()
    
    stats = {
        'monthly_attendance': month_attendance,
        'working_days': monthrange(today.year, today.month)[1],
        'leave_balance': 20 - total_leaves,  # Assuming 20 leaves per year
        'latest_salary': latest_payroll.net_salary if latest_payroll else 0
    }
    
    return render_template('dashboard/user.html', 
                         current_user=employee, 
                         stats=stats)
