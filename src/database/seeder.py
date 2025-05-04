from ..models.employee import Employee
from datetime import date

def seed_admin(db):
    admin = Employee.query.filter_by(username='admin').first()
    if not admin:
        admin = Employee(
            username='admin',
            name='Administrator',
            email='admin@example.com',
            position='Admin',
            salary=100000.0,
            base_salary=80000.0,
            hra=10000.0,
            da=5000.0,
            ta=5000.0,
            pf=2000.0,
            tax=3000.0,
            joining_date=date.today(),
            role='admin'
        )
        admin.set_password('123')
        db.session.add(admin)
        db.session.commit()
        print("Admin user created successfully!")
