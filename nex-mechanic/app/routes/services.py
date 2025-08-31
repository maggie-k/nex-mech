from flask import Blueprint, render_template
from app.extensions import db
from app.models import ReminderLog, UserCarProfile
from flask_login import current_user

bp= Blueprint('services', __name__, url_prefix='/services')

@bp.route('/')
def services():
    return render_template('service_cards.html')

@bp.route('/service_cards')
def service_categories():
    service_categories = [
        {
            "name": "Repair & Maintenance",
            "icon": "🛠️",
            "subcategories": [
                {"name": "Routine Maintenance", "description": "Keep your ride running smooth ⛽"},
                {"name": "Repairs & Diagnostics", "description": "Something off? Let’s fix it 🛠️"},
                {"name": "Tyres & Wheels", "description": "Grip the road with confidence 🛞"}
            ]
        },
        {
            "name": "Car Wash & Detailing",
            "icon": "✨",
            "subcategories": [
                {"name": "Exterior Wash", "description": "Shine on the outside"},
                {"name": "Interior Detail", "description": "Fresh on the inside"}
            ]
        },
        {
            "name": "Insurance & Compliance",
            "icon": "🛡️",
            "subcategories": [
                {"name": "Coverage Options", "description": "Stay covered"},
                {"name": "Inspections", "description": "Stay compliant"}
            ]
        },
        {
            "name": "On-Demand Services",
            "icon": "🚗",
            "subcategories": [
                {"name": "Mobile Services", "description": "We come to you — hassle free 🏠"},
                {"name": "Pickup & Drop-off", "description": "Too busy? We’ve got this 🚗➡️🏠"}
            ]
        }
    ]


    if not current_user.is_authenticated:
        return render_template('service_cards.html', car=None)

    # assume current user is available via Flask-Login

    car= UserCarProfile.query.filter_by(user_id= current_user.id).first()
    active_reminders= ReminderLog.query.filter_by(user_car_id= car.id, resolved=False).all()
    latest= active_reminders[0].reminder_text if active_reminders else ''



    return render_template('service_cards.html', service_categories=service_categories, popup_reminder=latest, reminder_count=len(active_reminders))

@bp.route('/<category>')
def subcategories(category):

	# show services for the selected category

	return render_template('sub-category.html', category= category)

