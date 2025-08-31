from flask import Blueprint, render_template, session, redirect, url_for, request
from app.extensions import db
from app.models import UserCarProfile, ServiceHistory, ReminderLog, db
from datetime import datetime, timedelta
from flask_login import current_user

bp= Blueprint('reminders', __name__, url_prefix='/reminders')

def generate_reminders_for_user(user_id):
	car_profiles= UserCarProfile.query.filter_by(user_id= user_id).all()


	for car in car_profiles:
		last_service= (
			ServiceHistory.query.filter_by(user_car_id= car.id)
			.order_by(ServiceHistory.service_date.desc())
			.first()
		)

		if not last_service:
			continue # No service history, skip for now

		mileage_diff= (car.current_mileage or 0)- (last_service.mileage_at_service or 0)

		days_since_service= (datetime.utcnow().date()- last_service.service_date).days

		
		# --- Mileage-based Reminder --->

		if mileage_diff>= 5000:
			reminder_text= "⛽ Time for an oil change or check-up (5,000 km passed)."

			# Avoid duplicate reminders

			exists= ReminderLog.query.filter_by(
				user_car_id= car.id,
				reminder_text= reminder_text,
				resolved=False
			).first()


			if not exists:
				db.session.add(ReminderLog(
					user_car_id=car.id,
					reminder_text=reminder_text
				))


		if days_since_service >=180:
			time_reminder= f"⏰ It's been {days_since_service} days since your last service. Consider a check-up."

			exists= ReminderLog.query.filter_by(
				user_car_id= car.id,
				reminder_text= reminder_text,
				resolved=False
			).first()

			if not exists:
				db.session.add(ReminderLog(
					user_car_id= car.id,
					reminder_text= reminder_text
				))

				# Send email function call


	db.session.commit()


@bp.route('/')
def view_reminders():

	if not current_user.is_authenticated:
		return render_template('reminders.html')

	# Get all car IDs owned by the current logged-in user

	car_ids= [car.id for car in UserCarProfile.query.filter_by(user_id=current_user.id)]

	# Get all unresolved reminders tied to those cars

	reminders= ReminderLog.query.filter(
		ReminderLog.user_car_id.in_(car_ids),
		ReminderLog.resolved== False
		).order_by(ReminderLog.created_at.desc()).all()


	return render_template('reminders.html', reminders= reminders)


@bp.route('/reminders/resolve/<int:reminder_id>', methods=['POST'])
def resolved_reminder(reminder_id):
	reminder= ReminderLog.query.get(reminder_id)
	if reminder:
		reminder.resolved= True
		db.session.commit()

	return redirect (url_for('reminders.view_reminders'))
