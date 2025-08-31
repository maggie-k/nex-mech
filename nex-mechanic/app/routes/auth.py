from flask import Blueprint, render_template

bp=	Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/login')
def login():
	return render_template('login.html')


@bp.route('sign_up')
def sign_up():
	return render_template('sign_up.html')

