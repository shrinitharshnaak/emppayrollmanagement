from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from ..models.attendance import Attendance
from ..models.employee import Employee
from ..models.leave import Leave  # Import the Leave model
from ..database import db
from datetime import datetime, date
from ..routes.auth import login_required, admin_required

attendance_bp = Blueprint('attendance', __name__, url_prefix='/attendance')

@attendance_bp.route('/record', methods=['GET', 'POST'])
@login_required
def record():
    today = date.today()
    employee_id = session.get('user_id')
    today_attendance = Attendance.query.filter_by(
        employee_id=employee_id,
        date=today
    ).first()
    
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'checkin' and not today_attendance:
            attendance = Attendance(
                employee_id=employee_id,
                date=today,
                time_in=datetime.now(),
                status='present'
            )
            db.session.add(attendance)
            flash('Attendance marked successfully', 'success')
        elif action == 'checkout' and today_attendance and not today_attendance.time_out:
            today_attendance.time_out = datetime.now()
            today_attendance.calculate_status()  # Dynamically calculate status
            flash('Check out time recorded', 'success')
        
        db.session.commit()
        return redirect(url_for('attendance.record'))
    
    # Get attendance history for the current user
    attendance_history = Attendance.query.filter_by(
        employee_id=employee_id
    ).order_by(Attendance.date.desc()).limit(10).all()
    
    return render_template('attendance/record.html',
                         today=today,
                         today_attendance=today_attendance,
                         attendance_history=attendance_history)

@attendance_bp.route('/report')
@admin_required
def report():
    month = request.args.get('month', datetime.now().month, type=int)
    year = request.args.get('year', datetime.now().year, type=int)
    
    attendances = Attendance.query.join(Employee).filter(
        db.extract('month', Attendance.date) == month,
        db.extract('year', Attendance.date) == year
    ).order_by(Employee.name, Attendance.date.desc()).all()
    
    return render_template('attendance/report.html', 
                         attendances=attendances,
                         current_month=month,
                         current_year=year)

def calculate_attendance_summary(employee_id, month, year):
    total_working_days = db.session.query(db.func.count(Attendance.id)).filter(
        Attendance.employee_id == employee_id,
        db.extract('month', Attendance.date) == month,
        db.extract('year', Attendance.date) == year
    ).scalar()

    present_days = db.session.query(db.func.count(Attendance.id)).filter(
        Attendance.employee_id == employee_id,
        Attendance.status == 'present',
        db.extract('month', Attendance.date) == month,
        db.extract('year', Attendance.date) == year
    ).scalar()

    leave_days = db.session.query(db.func.count(Leave.id)).filter(
        Leave.employee_id == employee_id,
        Leave.status == 'approved',
        db.extract('month', Leave.start_date) == month,
        db.extract('year', Leave.start_date) == year
    ).scalar()

    return total_working_days, present_days, leave_days