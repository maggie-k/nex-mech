#from flask_mail import Mail
from flask_mail import Message
from app.extensions import mail
from flask import current_app


def send_reminder_email(recipient, subject, body):
	with current_app.app_context():
		msg= Message(subject, recipients=[recipient])
		msg.body= body
		mail.send(msg)

	# call this after generating a new reminder
	# a reminder is generated
	# flask sends an email to the user's registered email address
