from flask import Blueprint, render_template, redirect, url_for, request, flash, session, Response
from werkzeug.security import check_password_hash, generate_password_hash
from ..models.employee import Employee
from ..database import db
from functools import wraps
from datetime import date
from typing import Callable, Any, Union

auth_bp = Blueprint('auth', __name__)

def login_required(f: Callable) -> Callable:
    @wraps(f)
    def decorated_function(*args: Any, **kwargs: Any) -> Union[Response, Any]:
        if 'user_id' not in session:
            flash('Please log in first.', 'danger')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f: Callable) -> Callable:
    @wraps(f)
    @login_required
    def decorated_function(*args: Any, **kwargs: Any) -> Union[Response, Any]:
        if not session.get('is_admin'):
            flash('Admin access required.', 'danger')
            return redirect(url_for('home'))
        return f(*args, **kwargs)
    return decorated_function

@auth_bp.route('/login', methods=['GET', 'POST'])
def login() -> Union[str, Response]:
    if request.method == 'POST':
        username: str = request.form['username']
        password: str = request.form['password']
        employee: Employee | None = Employee.query.filter_by(username=username).first()
        
        if employee and employee.check_password(password):
            session['user_id'] = employee.id
            session['is_admin'] = employee.role == 'admin'
            flash('Login successful!', 'success')
            # Redirect based on role
            if employee.role == 'admin':
                return redirect(url_for('admin.dashboard'))
            return redirect(url_for('user.dashboard'))
            
        flash('Invalid username or password', 'danger')
    return render_template('login.html')

@auth_bp.route('/logout')
def logout() -> Response:
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect(url_for('auth.login'))

@auth_bp.route('/register', methods=['GET', 'POST'])
def register() -> Union[str, Response]:
    if request.method == 'POST':
        username: str = request.form['username']
        email: str = request.form['email']
        password: str = request.form['password']
        name: str = request.form['name']
        role: str = request.form.get('role', 'user')
        
        # Check if username or email already exists
        if Employee.query.filter_by(username=username).first():
            flash('Username already exists', 'danger')
            return redirect(url_for('auth.register'))
        if Employee.query.filter_by(email=email).first():
            flash('Email already exists', 'danger')
            return redirect(url_for('auth.register'))
        
        employee = Employee(
            username=username,
            name=name,
            email=email,
            position='Staff',  # Default position
            salary=0.0,  # Default salary
            joining_date=date.today(),
            role=role
        )
        employee.set_password(password)
        
        db.session.add(employee)
        db.session.commit()
        
        flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('auth.login'))
        
    return render_template('register.html')