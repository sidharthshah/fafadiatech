import os 
import datetime
import simplejson as json
from mako.template import Template
from mako.lookup import TemplateLookup

tpl_lookup = TemplateLookup(directories=[os.path.join(os.path.dirname(__file__),"..","tpls")])

def userdashboard(request):
    tpl = tpl_lookup.get_template("expensecategorywise.html")
    return HttpResponse(tpl.render(csrf_token=c,on_home=True,project=allproject))

def adduser(request):
    pass

def modifyuser(request):
    pass 

def deleteuser(request):
    pass


