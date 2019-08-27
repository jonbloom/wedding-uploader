from peewee import SqliteDatabase
from dotenv import load_dotenv
import boto3
from tusclient import client
load_dotenv()
import os

DB_LOCATION = os.getenv('DB_LOCATION',)
S3_KEY = os.getenv('S3_KEY')
S3_SECRET = os.getenv('S3_SECRET')
S3_REGION = os.getenv('S3_REGION')
S3_ENDPOINT = os.getenv('S3_ENDPOINT')
S3_BUCKET = os.getenv('S3_BUCKET')
S3_ROOT_PATH = os.getenv('S3_ROOT_PATH')
S3_PUBLIC_PATH = os.getenv('S3_PUBLIC_PATH')

CLOUDFLARE_EMAIL = os.getenv('CLOUDFLARE_EMAIL')
CLOUDFLARE_API_KEY = os.getenv('CLOUDFLARE_API_KEY')
CLOUDFLARE_ACCOUNT_ID = os.getenv('CLOUDFLARE_ACCOUNT_ID')

SECRET_KEY = os.getenv('FLASK_SECRET_KEY')

ALLOWED_EXTENSIONS = set(['jpg', 'mp4', 'mov', 'png'])


s3_session = boto3.session.Session()
s3_client = s3_session.client('s3',
	region_name=S3_REGION,
	endpoint_url=S3_ENDPOINT,
	aws_access_key_id=S3_KEY,
	aws_secret_access_key=S3_SECRET)

cf_client = client.TusClient('https://api.cloudflare.com/client/v4/accounts/{account_id}/media'.format(account_id=CLOUDFLARE_ACCOUNT_ID),
                              headers={
                              'X-Auth-Email': CLOUDFLARE_EMAIL,
                              'X-Auth-Key': CLOUDFLARE_API_KEY
                              })


db = SqliteDatabase(DB_LOCATION)

if __name__ == '__main__':
	from uploader.models import create_tables
	create_tables()