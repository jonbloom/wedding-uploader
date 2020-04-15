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
		'uploads': [model_to_dict(u, backrefs=True, exclude=[User.uuid,User.is_admin, User.authenticated]) for u in Upload.select().order_by(Upload.timestamp.desc())]
	}
	return jsonify(uploads)

@api_bp.route('/cf_info/<uid>')
def get_cf_info(uid):
	return jsonify(cf_info(uid))

@api_bp.route('/upload/<upload_id>')
def upload_progress(upload_id):
	upload = Upload.get(uuid=upload_id)

	return jsonify(model_to_dict(upload, backrefs=True, exclude=[Upload.user]))

@api_bp.route('/upload/count')
def upload_count():
	uploads = Upload.select()
	return jsonify({'count': len(uploads)})

@api_bp.route('/upload/<upload_id>/report', methods=['POST'])
def report_upload(upload_id):
	upload = Upload.get(uuid=upload_id)
	upload.reported = True
	upload.save()
	return jsonify({'success': True})

@api_bp.route('/upload/<upload_id>/approve', methods=['POST'])
def approve_upload(upload_id):
	upload = Upload.get(uuid=upload_id)
	upload.reported = False
	upload.save()
	return jsonify({'success': True})

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
	rtn['success'] = True

	return jsonify(rtn)