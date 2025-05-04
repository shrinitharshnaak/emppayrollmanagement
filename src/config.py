import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-please-change'
    basedir = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'payroll.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

# Make sure Config is exported
__all__ = ['Config']
