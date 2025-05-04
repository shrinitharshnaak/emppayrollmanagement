from flask import Blueprint

from .auth import auth_bp
from .admin import admin_bp
from .user import user_bp
from .employee import employee_bp
from .attendance import attendance_bp
from .leave import leave_bp
from .payroll import payroll_bp

def init_routes(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(employee_bp)
    app.register_blueprint(attendance_bp)
    app.register_blueprint(leave_bp)
    app.register_blueprint(payroll_bp)