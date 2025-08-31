from flask import Blueprint, render_template, request, redirect, url_for
from app.extensions import db
from app.models import ReminderLog, UserCarProfile
from flask_login import current_user

bp= Blueprint('home', __name__)

@bp.route('/')
def splash():

	'''if not current_user.is_authenticated:
		return render_template('home.html', car=None)

	# assume current user is available via Flask-Login

	car= UserCarProfile.query.filter_by(user_id= current_user.id).first()
	active_reminders= ReminderLog.query.filter_by(user_car_id= car.id, resolved=False).all()
	latest= active_reminders[0].reminder_text if active_reminders else '''''


	return render_template('home.html')
	

@bp.route('/get-started', methods=['POST'])
def get_started():
	car_make= request.form.get('car_make')
	car_model= request.form.get('car_model')
	mileage= request.form.get('mileage')


	# save to session or database


	return redirect(url_for('services.service_categories'))

