from flask import Blueprint, request, redirect, url_for, render_template
from flask_login import login_user, login_required, logout_user, current_user
from uploader.models import User
from uploader.utils import *

user_bp = Blueprint('user', __name__)

@user_bp.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		email = request.form.get('email')
		first_name = request.form.get('first_name')
		last_name = request.form.get('last_name')
		try:
			user = User.get(first_name=first_name, last_name=last_name)
			print('found user')
		except User.DoesNotExist:
			user = User()
			user.first_name = first_name
			user.last_name = last_name
			print('new user')
			user.save(force_insert=True)
		user.authenticated = True
		user.save()
		login_user(user)
		return redirect(url_for('uploads.list'))
	else:
		return render_template('user/login.html')