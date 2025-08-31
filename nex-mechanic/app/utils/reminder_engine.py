from datetime import datetime, timedelta
from app.utils.email_utils import send_reminder_email
from app.extensions import db
from app.models import UserCarProfile, ServiceHistory, ReminderLog


def generate_reminders():
	cars= UserCarProfile.query.all()

	for car in cars:
		last_service= ServiceHistory.query.filter_by(user_car_id=car.id).order_by(ServiceHistory.service_date.desc()).first()
		
		if not last_service:
			continue


		# Mileage-based

		mileage_gap=5000
		if car.current_mileage and (car.current_mileage - last_service.mileage_at_service >= mileage_gap):
			add_reminder(car.id, f"Time for a service: you've driven {mileage_gap})km since your last one.")


		# Time-based (6 months)

		months_passed= (datetime.utcnow().date() - last_service.service_date).days
		if months_passed >= 180:
			add_reminder(car.id, "It's been 6+ months sice your last service.")

def add_reminder(car_id, message):
	
	# Avoid duplicates

	existing= ReminderLog.query.filter_by(user_car_id=car_id, reminder_text=message, resolved=False).first()

	if not existing:
		db.session.add(ReminderLog(user_car_id= car_id, reminder_text=message))
		
		# Send email 

		






		db.session.commit()

