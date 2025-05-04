from flask import Blueprint, render_template, redirect, url_for, request, flash
from ..models.employee import Employee
from ..database import db
from ..routes.auth import admin_required
from datetime import datetime

employee_bp = Blueprint('employee', __name__, url_prefix='/employees')

@employee_bp.route('/')
def list():
    employees = Employee.query.all()
    return render_template('employees/list.html', employees=employees)

@employee_bp.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        try:
            employee = Employee(
                username=request.form['username'],
                name=request.form['name'],
                email=request.form['email'],
                position=request.form['position'],
                salary=float(request.form['salary']),
                base_salary=float(request.form['base_salary']),
                hra=float(request.form.get('hra', 0)),
                da=float(request.form.get('da', 0)),
                ta=float(request.form.get('ta', 0)),
                pf=float(request.form.get('pf', 0)),
                tax=float(request.form.get('tax', 0)),
                joining_date=datetime.strptime(request.form['joining_date'], '%Y-%m-%d').date(),
                role='user'
            )
            employee.set_password(request.form['password'])
            db.session.add(employee)
            db.session.commit()
            flash('Employee added successfully', 'success')
            return redirect(url_for('employee.list'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding employee: {str(e)}', 'danger')
            return render_template('employees/add.html')
            
    return render_template('employees/add.html')

@employee_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@admin_required
def edit(id):
    employee = Employee.query.get_or_404(id)
    if request.method == 'POST':
        try:
            employee.username = request.form['username']
            employee.name = request.form['name']
            employee.email = request.form['email']
            employee.position = request.form['position']
            employee.salary = float(request.form['salary'])
            employee.base_salary = float(request.form['base_salary'])
            employee.hra = float(request.form.get('hra', 0))
            employee.da = float(request.form.get('da', 0))
            employee.ta = float(request.form.get('ta', 0))
            employee.pf = float(request.form.get('pf', 0))
            employee.tax = float(request.form.get('tax', 0))
            employee.joining_date = datetime.strptime(request.form['joining_date'], '%Y-%m-%d').date()
            
            if request.form.get('password'):
                employee.set_password(request.form['password'])
            
            db.session.commit()
            flash('Employee updated successfully', 'success')
            return redirect(url_for('employee.list'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating employee: {str(e)}', 'danger')
            
    return render_template('employees/edit.html', employee=employee)