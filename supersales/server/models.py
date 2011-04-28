from google.appengine.ext import db 

class UserProfile(db.Model):
	name = db.StringProperty(required=True)
	email = db.StringProperty(required=True)
	passwd = db.EmailProperty(required=True)