from peewee import *
from .config import db, S3_PUBLIC_PATH
from uuid import uuid4
import datetime


class BaseModel(Model):
	class Meta:
		database = db


class User(BaseModel):
	uuid = TextField(unique=True, primary_key=True, default=uuid4)
	email = TextField(unique=True)
	first_name = TextField()
	last_name = TextField()
	is_admin = BooleanField(default=False)
	authenticated = BooleanField(default=False)

	def is_active(self):
		return True

	def is_anonymous(self):
		return False

	def is_authenticated(self):
		return self.authenticated

	def get_id(self):
		return str(self.uuid)

class Upload(BaseModel):
	uuid = TextField(unique=True, primary_key=True, default=uuid4)
	user = ForeignKeyField(User, backref="uploads")
	title = TextField()
	timestamp = DateTimeField(default=datetime.datetime.now)
	total_files = IntegerField(default=0)
	uploaded_files = IntegerField(default=0)
	
class File(BaseModel):
	uuid = TextField(unique=True, primary_key=True, default=uuid4)
	media_type=TextField()
	upload = ForeignKeyField(Upload, backref="files")
	s3_key = TextField()
	cf_uid = TextField(null=True)
	

	def get_s3_url(self):
		return S3_PUBLIC_PATH+self.s3_key


def create_tables():
	db.create_tables([User, Upload, File], safe=True)