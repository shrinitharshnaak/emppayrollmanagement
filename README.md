# 🏢 Payroll Management System

A modern, web-based payroll management solution built with Python Flask and SQLite3. This system simplifies payroll processing, attendance tracking, and leave management for organizations of all sizes.

## ✨ Features

### 👥 User Management
- Role-based access control (Admin/Employee)
- Secure authentication system
- Profile management and updates

### 👔 Employee Management
- Add, edit, and list employee profiles
- Salary structure configuration
- Department and role organization

### ⏰ Attendance System
- Daily attendance tracking
- Check-in/Check-out recording
- Monthly attendance reports
- Overtime calculation

### 📅 Leave Management
- Leave requests and approvals
- Multiple leave types (e.g., sick leave, vacation)
- Leave balance tracking
- Leave history and reporting

### 💰 Payroll Processing
- Automated salary calculation
- Deductions and allowances
- Tax calculations
- Payslip generation
- Monthly payroll reports

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip package manager
- Virtual environment (recommended)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/payroll-management.git
   cd payroll-management
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Initialize the database:
   ```bash
   python -m src.initdb
   ```

5. Seed the database with an admin user:
   ```bash
   python -m src.database.seeder
   ```

6. Start the application:
   ```bash
   python -m src.app
   ```

The application will be available at `http://localhost:5000`.

### Default Admin Credentials
- **Username**: `admin`
- **Password**: `123`

## 🛠️ Technology Stack

- **Backend**: Python Flask
- **Database**: SQLite3
- **Frontend**: HTML5, CSS3, JavaScript
- **Icons**: Feather Icons
- **UI Framework**: Custom CSS

## 📁 Project Structure
   ```bash
payroll-management/
├── src/
│   ├── static/
│   │   ├── styles/
│   │   └── scripts/
│   ├── templates/
│   │   ├── auth/
│   │   ├── dashboard/
│   │   ├── employee/
│   │   ├── attendance/
│   │   ├── leave/
│   │   └── payroll/
│   ├── models/
│   ├── routes/
│   ├── database/
│   └── app.py
├── tests/
├── requirements.txt
└── README.md
   ```

🔒 Security Features
Password hashing using bcrypt
CSRF protection
Session management
Role-based access control
Input validation and sanitization
📱 Responsive Design
The application is fully responsive and works seamlessly on:

💻 Desktop computers
💪 Tablets
📱 Mobile devices
🤝 Contributing
Fork the repository.
Create a feature branch (git checkout -b feature/AmazingFeature).
Commit your changes (git commit -m 'Add AmazingFeature').
Push to the branch (git push origin feature/AmazingFeature).
Open a Pull Request.
📝 License
This project is licensed under the MIT License. See the LICENSE file for details.

🙏 Acknowledgments
Flask framework documentation
SQLAlchemy documentation
Feather Icons
Open-source contributors
