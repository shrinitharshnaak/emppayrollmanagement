from flask import Blueprint, render_template, session, request, flash, redirect, url_for
from ..models.employee import Employee
from ..models.attendance import Attendance
from ..models.leave import Leave
from ..models.payroll import Payroll
from ..routes.auth import login_required
from ..database import db
from werkzeug.security import check_password_hash
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
    
    # Get today's attendance
    today_attendance = Attendance.query.filter_by(
        employee_id=employee.id,
        date=today
    ).first()
    
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
                         stats=stats,
                         today=today,
                         today_attendance=today_attendance)

@user_bp.route('/profile')
@login_required
def profile():
    employee = Employee.query.get(session['user_id'])
    return render_template('user/profile.html', user=employee)

@user_bp.route('/settings')
@login_required
def settings():
    employee = Employee.query.get(session['user_id'])
    return render_template('user/settings.html', user=employee)

@user_bp.route('/update-profile', methods=['POST'])
@login_required
def update_profile():
    employee = Employee.query.get(session['user_id'])
    if employee:
        try:
            employee.name = request.form['name']
            employee.email = request.form['email']
            db.session.commit()
            flash('Profile updated successfully', 'success')
        except Exception as e:
            db.session.rollback()
            flash('Error updating profile', 'danger')
    return redirect(url_for('user.settings'))

@user_bp.route('/change-password', methods=['POST'])
@login_required
def change_password():
    employee = Employee.query.get(session['user_id'])
    if employee:
        current_password = request.form['current_password']
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']

        if not employee.check_password(current_password):
            flash('Current password is incorrect', 'danger')
        elif new_password != confirm_password:
            flash('New passwords do not match', 'danger')
        else:
            try:
                employee.set_password(new_password)
                db.session.commit()
                flash('Password updated successfully', 'success')
            except Exception as e:
                db.session.rollback()
                flash('Error updating password', 'danger')

    return redirect(url_for('user.settings'))
