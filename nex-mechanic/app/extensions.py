from flask_sqlalchemy import SQLAlchemy
from flask_apscheduler import APScheduler
from flask_mail import Mail


db= SQLAlchemy()

scheduler= APScheduler()

mail=Mail()

