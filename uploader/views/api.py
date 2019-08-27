from flask import Blueprint, jsonify
from flask_login import login_user, login_required, logout_user, current_user
from uploader.models import User, Upload, File
from playhouse.shortcuts import model_to_dict
from uploader.utils import *
import random

api_bp = Blueprint('api', __name__)

@api_bp.route('/uploads')
def list_uploads():
	uploads = {
		'uploads': [model_to_dict(u, backrefs=True, exclude=[User.uuid, User.email, User.is_admin, User.authenticated]) for u in Upload.select()]
	}
	for upload in uploads['uploads']:
		for file in upload['files']:
			if file['media_type'] == 'video':
				file['cf_data'] = cf_info(file['cf_uid'])
	return jsonify(uploads)