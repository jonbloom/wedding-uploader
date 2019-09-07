from .config import S3_BUCKET, S3_ROOT_PATH, S3_PUBLIC_PATH, ALLOWED_EXTENSIONS, CLOUDFLARE_API_KEY, CLOUDFLARE_EMAIL, CLOUDFLARE_ACCOUNT_ID, s3_client, cf_client
from flask_login import current_user
from flask import flash
from uuid import uuid4
import requests

def success(text):
	flash(text,'success')

def warn(text):
	flash(text,'warning')

def fail(text):
	flash(text,'danger')

def allowed_file(file):
	allowed = False
	if len(file.filename) == 0:
		return allowed
	filename = file.filename
	extension = filename.rsplit('.', 1)[1].lower()
	print(extension)
	allowed = '.' in filename and extension in ALLOWED_EXTENSIONS
	if not allowed:
		warn('Image must be of type: {0}'.format(', '.join(ALLOWED_EXTENSIONS)))
	return allowed

def upload_to_s3(to_upload):
	key = get_filename(to_upload, uuid4())
	s3_client.upload_fileobj(to_upload, S3_BUCKET, key, ExtraArgs={'ContentType': to_upload.mimetype})
	set_permissions(key)
	return key

def upload_to_cf(url, title):
	headers = {
		'X-Auth-Key': CLOUDFLARE_API_KEY,
		'X-Auth-Email': CLOUDFLARE_EMAIL,
	}
	json = {
		'url': url,
		'meta': {
			'name': title
		}
	}
	req = requests.post('https://api.cloudflare.com/client/v4/accounts/{account_id}/stream/copy'.format(account_id=CLOUDFLARE_ACCOUNT_ID), headers=headers, json=json)
	return req.json()['result']['uid']

def delete_from_cf(uid):
	headers = {
		'X-Auth-Key': CLOUDFLARE_API_KEY,
		'X-Auth-Email': CLOUDFLARE_EMAIL,
	}
	req = requests.delete('https://api.cloudflare.com/client/v4/accounts/{account_id}/media/{media_uid}'.format(account_id=CLOUDFLARE_ACCOUNT_ID, media_uid=uid), headers=headers, json=json)
	return req.status_code == 200

def cf_info(uid):
	headers = {
		'X-Auth-Key': CLOUDFLARE_API_KEY,
		'X-Auth-Email': CLOUDFLARE_EMAIL,
	}
	req = requests.get('https://api.cloudflare.com/client/v4/accounts/{account_id}/media/{video_id}'.format(account_id=CLOUDFLARE_ACCOUNT_ID, video_id=uid), headers=headers)
	return req.json()


def delete_file(file):
	s3_client.delete_object(Bucket=S3_BUCKET, Key=file.s3_key)
	if file.media_type == 'video':
		headers = {
			'X-Auth-Key': CLOUDFLARE_API_KEY,
			'X-Auth-Email': CLOUDFLARE_EMAIL,
		}
		req = requests.delete('https://api.cloudflare.com/client/v4/accounts/{account_id}/media/{media_uid}'.format(account_id=CLOUDFLARE_ACCOUNT_ID, media_uid=file.cf_uid), headers=headers)
		return req.status_code == 200
	return True

def set_permissions(key_name):
	s3_client.put_object_acl(ACL='public-read', Bucket=S3_BUCKET, Key=key_name)

def get_filename(file, new_name):
	extension = file.filename.rsplit('.', 1)[1]
	return '{0}/{1}.{2}'.format(S3_ROOT_PATH, new_name, extension.lower())