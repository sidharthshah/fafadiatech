import os 
import datetime
import simplejson as json
from mako.template import Template
from mako.lookup import TemplateLookup
from django.core.context_processors import csrf
from django.http import HttpResponseRedirect, HttpResponse
from alfredapp.models import *

tpl_lookup = TemplateLookup(directories=[os.path.join(os.path.dirname(__file__),"..","tpls")])

def userdashboard(request):
    c = request.COOKIES.get('csrftoken','')
    tpl = tpl_lookup.get_template("usrsummry.html")
    user = Alfreduser.objects.all()
    #status = TicketStatus.objects.all()
    return HttpResponse(tpl.render(csrf_token=c,on_home=True,status=[],User=user,userName='Smita'))

def adduser(request):
    pass

def modifyuser(request):
    pass 

def deleteuser(request):
    pass


def customersummary(request):
    c = request.COOKIES.get('csrftoken','')
    tpl = tpl_lookup.get_template("customersummary.html")

