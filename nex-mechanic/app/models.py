from app.extensions import db 
from flask_login import UserMixin
from sqlalchemy import func
from datetime import datetime


class UserCarProfile(db.Model, UserMixin):
	id= db.Column(db.Integer, primary_key=True)
	user_id= db.Column(db.Integer, nullable=False) # link to auth table
	car_make= db.Column(db.String(50), nullable=False)
	car_model= db.Column(db.String(50), nullable=False)
	current_mileage= db.Column(db.Integer, nullable= True)
	last_updated= db.Column(db.DateTime, default= datetime.utcnow)

	def __repr__(self):
		return f'<UserCarProfile {self.car_make} {self.car_model}>'


class ServiceHistory(db.Model):
	id= db.Column(db.Integer, primary_key=True)
	user_car_id= db.Column(db.Integer, db.ForeignKey('user_car_profile.id'), nullable=False)
	service_type= db.Column(db.String(100), nullable=False) # e.g. 'Oil Change'
	mileage_at_service= db.Column(db.Integer, nullable=False)
	service_date= db.Column(db.Date, default= datetime.utcnow)
	notes= db.Column(db.Text, nullable=True)

	def __repr__(self):
		return f'<ServiceHistory {self.service_type} at {self.mileage_at_service}km>'


class ReminderLog(db.Model):
	id= db.Column(db.Integer, primary_key=True)
	user_car_id= db.Column(db.Integer, db.ForeignKey('user_car_profile.id'), nullable=False)
	reminder_text= db.Column(db.String(255), nullable=False)
	created_at= db.Column(db.DateTime, default= datetime.utcnow)
	resolved= db.Column(db.Boolean, default=False)

	def __repr__(self):
		return f'<Reminder {self.reminder_text}>'

