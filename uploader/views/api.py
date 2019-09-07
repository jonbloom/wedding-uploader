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
		'uploads': [model_to_dict(u, backrefs=True, exclude=[User.uuid, User.email, User.is_admin, User.authenticated]) for u in Upload.select().order_by(Upload.timestamp.desc())]
	}
	for upload in uploads['uploads']:
		for file in upload['files']:
			if file['media_type'] == 'video':
				file['cf_data'] = cf_info(file['cf_uid'])
	return jsonify(uploads)

@api_bp.route('/upload/<upload_id>', methods=['DELETE'])
def delete_upload(upload_id):
	rtn = {
		'success': False,
		'deleted': 0
	}
	upload = Upload.get(uuid=upload_id)
	print(upload)
	for file in upload.files:
		print('deleting file: {0}'.format(file.uuid))
		print(delete_file(file))
		file.delete_instance()
		rtn['deleted'] += 1
	upload.delete_instance()

	return jsonify(rtn)