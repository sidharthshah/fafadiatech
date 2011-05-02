from google.appengine.ext import db 

class UserProfile(db.Model):
	name = db.StringProperty(required=True)
	email = db.EmailProperty(required=True)
	passwd = db.StringProperty(required=True)

class Lead(db.Model):
	ts = db.DateTimeProperty(required=True)
	name = db.StringProperty(required=True)
	contactperson = db.StringProperty(required=True)
	contactnumber = db.StringProperty(required=True)
	area = db.StringProperty(required=True)
	email = db.EmailProperty()
	status = db.StringProperty()
	user = db.EmailProperty()
