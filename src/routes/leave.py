from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from ..models.leave import Leave
from ..database import db
from datetime import datetime, date
from ..routes.auth import login_required, admin_required

leave_bp = Blueprint('leave', __name__, url_prefix='/leave')

@leave_bp.route('/request', methods=['GET', 'POST'])
@login_required
def request_leave():
    today = date.today().strftime('%Y-%m-%d')
    if request.method == 'POST':
        employee_id = session.get('user_id')  # Get employee_id from session
        leave = Leave(
            employee_id=employee_id,
            start_date=datetime.strptime(request.form['start_date'], '%Y-%m-%d').date(),
            end_date=datetime.strptime(request.form['end_date'], '%Y-%m-%d').date(),
            reason=request.form['reason']
        )
        db.session.add(leave)
        db.session.commit()
        flash('Leave request submitted successfully', 'success')
        return redirect(url_for('leave.request_leave'))
    return render_template('leave/request.html', today=today)

@leave_bp.route('/list')
@admin_required
def list_requests():
    leaves = Leave.query.all()
    return render_template('leave/approve.html', leaves=leaves)

@leave_bp.route('/approve/<int:id>', methods=['POST'])
@admin_required
def approve(id):
    leave = Leave.query.get_or_404(id)
    leave.status = request.form['status']
    db.session.commit()
    flash('Leave request updated', 'success')
    return redirect(url_for('leave.list_requests'))