from flask import Blueprint, render_template
from ..models.employee import Employee
from ..models.attendance import Attendance
from ..models.leave import Leave
from ..models.payroll import Payroll
from ..routes.auth import admin_required
from datetime import datetime, date

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/dashboard')
@admin_required
def dashboard():
    today = date.today()
    
    stats = {
        'total_employees': Employee.query.count(),
        'today_attendance': Attendance.query.filter_by(
            date=today,
            status='present'
        ).count(),
        'pending_leaves': Leave.query.filter_by(status='pending').count(),
        'monthly_payroll': sum(p.net_salary for p in Payroll.query.filter(
            Payroll.month == today.month,
            Payroll.year == today.year
        ).all())
    }
    
    # Get recent activities with consistent datetime objects
    activities = []
    
    # Add leave requests
    recent_leaves = Leave.query.order_by(Leave.id.desc()).limit(5).all()
    for leave in recent_leaves:
        activities.append({
            'timestamp': datetime.combine(leave.start_date, datetime.min.time()),
            'type': 'Leave Request',
            'details': f'{leave.employee.name} - {leave.status}'
        })
    
    # Add attendance records
    recent_attendance = Attendance.query.order_by(Attendance.id.desc()).limit(5).all()
    for attendance in recent_attendance:
        activities.append({
            'timestamp': datetime.combine(attendance.date, attendance.time_in.time() if attendance.time_in else datetime.min.time()),
            'type': 'Attendance',
            'details': f'{attendance.employee.name} - {attendance.status}'
        })
    
    # Sort activities by timestamp
    activities.sort(key=lambda x: x['timestamp'], reverse=True)
    
    return render_template('dashboard/admin.html', 
                         stats=stats, 
                         activities=activities[:10])
