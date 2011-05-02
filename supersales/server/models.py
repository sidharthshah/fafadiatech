from google.appengine.ext import db 

class UserProfile(db.Model):
	name = db.StringProperty(required=True)
	email = db.EmailProperty(required=True)
	passwd = db.StringProperty(required=True)

class Lead(db.Model):
	ts = db.DateTimeProperty()
	name = db.StringProperty(required=True)
	contactperson = db.StringProperty()
	contactnumber = db.StringProperty()
	area = db.StringProperty()
	email = db.EmailProperty()
	status = db.StringProperty()
	user = db.EmailProperty()
	lat = db.StringProperty()
	lng = db.StringProperty()
