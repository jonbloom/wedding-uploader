from flask import Blueprint, request, redirect, url_for, render_template
from flask_login import login_user, login_required, logout_user, current_user
from uploader.models import User, Upload, File
from uploader.utils import *
from uploader.config import S3_PUBLIC_PATH
import random

uploads_bp = Blueprint('uploads', __name__)


def random_size():
	return random.randint(400,600)

@uploads_bp.route('/')
def list():
	uploads = Upload.select()
	return render_template('uploads/list.html', uploads=uploads, random_size=random_size, S3_PUBLIC_PATH=S3_PUBLIC_PATH)

@uploads_bp.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
	if request.method == 'POST':
		_upload = Upload()
		_upload.user = current_user.uuid
		_upload.title = request.form.get('title')
		_upload.total_files = len(request.files.getlist('media'))
		_upload.save(force_insert=True)

		if 'media' in request.files:
			for i, file in enumerate(request.files.getlist('media')):
				print(i)
				if allowed_file(file):
					print('allowed', file.filename)
					_file = File()
					_file.upload = _upload
					_file.s3_key = upload_to_s3(file)
					if file.filename.lower().endswith('.mp4') or file.filename.lower().endswith('.mov'):
						_file.media_type = 'video'
						_file.cf_uid = upload_to_cf(_file.get_s3_url(), _upload.title)
					else:
						_file.media_type = 'image'
					_file.save(force_insert=True)
					_upload.uploaded_files = _upload.uploaded_files + 1
					_upload.save()
				success('Media uploaded successfully.')
			return redirect(url_for('.list'))
	return render_template('uploads/upload.html')