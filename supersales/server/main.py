from google.appengine.ext import db 
from google.appengine.ext import webapp 
from google.appengine.ext.webapp.util import run_wsgi_app 

from models import *

class MainPage(webapp.RequestHandler):
	def get(self):
		self.response.headers['Content-Type'] = 'text/plain'
		self.response.out.write('Hello, Super Sales')

class AddUser(webapp.RequestHandler):
	def post(self):
		try:
			uname = self.request.get('name')
			uemail = self.request.get('email')
			upasswd = self.request.get('passwd')

			user = UserProfile(name=uname,email=uemail,passwd=upasswd)
			user.put()

			self.response.headers['Content-Type'] = 'text/plain'
			self.response.out.write("1")
		except:
			self.response.headers['Content-Type'] = 'text/plain'
			self.response.out.write("-1")

class AuthUser(webapp.RequestHandler):
	def post(self):
		try:
			uemail = self.request.get('email')
			upasswd = self.request.get('passwd')
			
			q = "WHERE email = '%s' AND passwd = '%s'" % (uemail,upasswd)

			result = UserProfile.gql(q)
			status = ""
			
			if(result.count() == 1):
				status = "1"
			else:
				status = "0"

			self.response.headers['Content-Type'] = 'text/plain'
			self.response.out.write(status)
						
		except:
			self.response.headers['Content-Type'] = 'text/plain'
			self.response.out.write("-1")			

application = webapp.WSGIApplication([('/',MainPage),('/users/add',AddUser),('/users/auth',AuthUser),],debug=True)

def main():
	run_wsgi_app(application)

if __name__ == "__main__":
	main()