import os 
import datetime
import simplejson as json
from mako.template import Template
from mako.lookup import TemplateLookup
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect, HttpResponse
from alfredapp.models import *

tpl_lookup = TemplateLookup(directories=[os.path.join(os.path.dirname(__file__),"..","tpls")])

def userdashboard(request):
    c = request.COOKIES.get('csrftoken','')
    tpl = tpl_lookup.get_template("usrsummry.html")
    user = Alfreduser.objects.all()
    status = TicketStatus.objects.all()
    return HttpResponse(tpl.render(csrf_token=c,on_home=True,status=status,User=user,userName='Smita'))

def adduserform(request):
    c = request.COOKIES.get('csrftoken','')
    tpl = tpl_lookup.get_template("usr_add.html")
    user = Alfreduser.objects.all()
    status = TicketStatus.objects.all()
    return HttpResponse(tpl.render(csrf_token=c,on_home=True,status=status,User=user,userName='Smita'))

def useradd(request):
    ts = datetime.datetime.now()
    username = request.POST.get('username')
    password = request.POST.get('password')
    usertype = request.POST.get('usertype')
    userobj = Alfreduser(Username=username,Password=password,Datejoined=ts,Usertype=usertype)
    userobj.save()

def usereditform(request):
    c = request.COOKIES.get('csrftoken','')
    tpl = tpl_lookup.get_template("edituser.html")
    user = Alfreduser.objects.all()
    status = TicketStatus.objects.all()
    return HttpResponse(tpl.render(csrf_token=c,on_home=True,status=status,User=user,userName='Smita'))
   
    
def modifyuser(request):
    pass 

def deleteuser(request):
    pass

def teamdashboard(request):
    c = request.COOKIES.get('csrftoken','')
    tpl = tpl_lookup.get_template("teamsummary.html")
    team = Team.objects.all()
    status = TicketStatus.objects.all()
    return HttpResponse(tpl.render(csrf_token=c,on_home=True,status=status,team=team,userName='Smita'))


def addteamform(request):
    c = request.COOKIES.get('csrftoken','')
    tpl = tpl_lookup.get_template("createteam.html")
    user = Alfreduser.objects.all()
    status = TicketStatus.objects.all()
    return HttpResponse(tpl.render(csrf_token=c,on_home=True,status=status,User=user,userName='Smita'))

@csrf_exempt
def teamadd(request):
    name = request.POST.get('name')
    address = request.POST.get('address')
    landline = request.POST.get('landline')
    mobile = request.POST.get('mobile')
    email = request.POST.get('email')
    try:    
        teamobj = Team(name=name,address=address,landlineno=landline,mobileno=mobile,email=email)
        teamobj.save()
        return HttpResponse(str(1))   
    except:
        return HttpResponse(str(0))    
        

def teameditform(request):
    c = request.COOKIES.get('csrftoken','')
    tpl = tpl_lookup.get_template("editteam.html")
    teamid = request.POST.get('teamid')
    team = Team.objects.filter(id=teamid)
    status = TicketStatus.objects.all()
    return HttpResponse(tpl.render(csrf_token=c,on_home=True,team=team,status=status,User=user,userName='Smita'))
   
    
def modifyteam(request):
    teamid = request.POST.get('id')
    name = request.POST.get('name')
    address = request.POST.get('address')
    landlineno = request.POST.get('landlineno')
    mobileno = request.POST.get('mobileno')
    email = request.POST.get('email')
    try:
        obj = Team.objects.filter(id=teamid).update(name=name,address=address,landlineno=landlineno,mobileno=mobileno,email=email)
        return HttpResponse(str(1))
    except:
        return HttpResponse(str(0))
  

def deleteteam(request):
    teamid = request.POST.get('id')
    try:
        Team.objects.filter(id=teamid).delete()
        return HttpResponse(str(1))
    except:
        return HttpResponse(str(0))
    
def departmentdashboard(request):
    c = request.COOKIES.get('csrftoken','')
    tpl = tpl_lookup.get_template("issuemaster.html")
    status = TicketStatus.objects.all()
    deparment = Deparment.objects.all() 
    return HttpResponse(tpl.render(csrf_token=c,on_home=True,status=status,deparment=deparment,userName='Smita'))


@csrf_exempt
def departmentadd(request):
    c = request.COOKIES.get('csrftoken','')
    department = request.POST.get('department')
    try:      
        deptobj = Deparment(department=department)
        deptobj.save()
        return HttpResponse(str(1))   
    except:
        return HttpResponse(str(0))
    
def departmentedit(request):
    c = request.COOKIES.get('csrftoken','')
    deptid = request.GET.get('deptid')
    try:
        deptobj = Deparment.objects.filter(id=deptid)
    except:
        deptobj = None
    tpl = tpl_lookup.get_template("editissuemaster.html")
    status = TicketStatus.objects.all()
    return HttpResponse(tpl.render(csrf_token=c,on_home=True,status=status,dept=deptobj[0],userName='Smita'))

@csrf_exempt
def modifydepartment(request):
    c = request.COOKIES.get('csrftoken','')
    deptid = request.POST.get('deptid')
    dept = request.POST.get('dept')
    obj = Deparment.objects.filter(id=deptid).update(department=dept)
    return HttpResponse(str(obj))

   
@csrf_exempt
def deletedepartment(request):
    c = request.COOKIES.get('csrftoken','')
    deptid = request.POST.get('deptid')
    try:
        obj = Deparment.objects.filter(id=deptid).delete()
        return HttpResponse(str(1))
    except:
        return HttpResponse(str(0))

def customersummary(request):
    c = request.COOKIES.get('csrftoken','')
    tpl = tpl_lookup.get_template("customersummary.html")

