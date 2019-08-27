from flask import Flask, request, redirect, url_for
from flask_login import LoginManager, login_required
from .models import User


app = Flask(__name__)
app.config.from_object('uploader.config')



login_manager = LoginManager()
login_manager.login_view = "user.login"
login_manager.login_message_category = "warning"
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
	try:
		return User.get(uuid=user_id)
	except User.DoesNotExist:
		return None


@app.before_request
def before_request():
	try:
		db.connect()
	except:
		pass

@app.teardown_request
def teardown_request(exception):
	try:
		db.close()
	except:
		pass

from .views.user import user_bp
from .views.uploads import uploads_bp
from .views.api import api_bp
app.register_blueprint(user_bp, url_prefix="/user")
app.register_blueprint(uploads_bp, url_prefix="/uploads")
app.register_blueprint(api_bp, url_prefix="/api")

@app.route('/')
def default_route():
	return redirect(url_for('uploads.list'))
