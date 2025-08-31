from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.extensions import db
from app.extensions import mail
from flask_login import LoginManager
from app.extensions import scheduler
from app.utils.reminder_engine import generate_reminders
from .routes import home, services, auth, cart, reminders, upload_docs



DB_NAME='database.db'

def create_app():
	app= Flask(__name__)
	app.config.from_object('config')
	app.config['SECRET_KEY'] = 'secret'
	app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
	app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

	@app.after_request
	def skip_ngrok_warning(response):
		response.headers["ngrok-skip-browser-warning"]= "true"
		return response
	
	db.init_app(app)

	mail.init_app(app)

	scheduler.init_app(app)
	scheduler.start()

	# Scheduler reminder job to run daily at 2am

	scheduler.add_job(id='daily-reminders', func=generate_reminders, trigger='interval', hours=24)

	# Register blueprints

	app.register_blueprint(home.bp)
	app.register_blueprint(services.bp)
	app.register_blueprint(auth.bp)
	app.register_blueprint(cart.bp)
	app.register_blueprint(reminders.bp)
	app.register_blueprint(upload_docs.bp)

	from .models import UserCarProfile, ServiceHistory, ReminderLog


	login_manager=LoginManager()
	login_manager.init_app(app)

	@login_manager.user_loader
	def load_user(id):
		return UserCarProfile.query.get(int(id))

	return app


