import os
import urllib
import datetime
from time import gmtime, strftime
import simplejson as json
from mako.template import Template
from mako.lookup import TemplateLookup
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.sessions.models import Session
from django.contrib.sessions.backends.db import SessionStore
from alfredapp.models import *

from django.conf import settings
from django.contrib.auth.models import User, check_password


tpl_lookup = TemplateLookup(directories=[os.path.join(os.path.dirname(__file__),"..","tpls")])


def getUserDetails(request,uname,passwd):
    allteamuser = Team.objects.all()
    allcustomer =  Customer.objects.all()   
    for i in allteamuser:
        if i.username == uname and i.password==passwd:
            return i
    for j in allcustomer:
        if j.username == uname and j.password==passwd:
            return j
    return None
    

def home(request):
    try:
        s = Session.objects.get(pk=request.session.session_key)
        s.delete()
        c = request.COOKIES.get('csrftoken','')
        tpl = tpl_lookup.get_template("login.html")
        user = Alfreduser.objects.all()
        status = TicketStatus.objects.all()
        return HttpResponse(tpl.render(csrf_token=c,on_home=True,uname="status",password="user",unamemsg="dfdfdf",pmsg="",msg="",userName='Smita'))
    except:
        c = request.COOKIES.get('csrftoken','')
        tpl = tpl_lookup.get_template("login.html")
        user = Alfreduser.objects.all()
        status = TicketStatus.objects.all()
        return HttpResponse(tpl.render(csrf_token=c,on_home=True,uname="status",password="user",unamemsg="dfdfdf",pmsg="",msg="",userName='Smita'))

def useredit(request):
    pass

@csrf_exempt
def userdelete(request):
    c = request.COOKIES.get('csrftoken','')
    

@csrf_exempt
def login(request):
    c = request.COOKIES.get('csrftoken','')
    username = request.POST.get('username')
    password = request.POST.get('password')
    userobj = getUserDetails(request,username,password)
    print userobj
    if userobj: 
        request.session.set_expiry(1800)
        request.session['userid']=urllib.quote(str(userobj.id))
        request.session['last_login'] = datetime.datetime.now()
        request.session['myname'] = urllib.quote(userobj.username)
        try:
            request.session['department'] = urllib.quote(str(userobj.department.department))
        except:
            request.session['department'] = "customer"
        try:
            request.session['type'] = urllib.quote(userobj.usertype)
        except:
            request.session['type'] = urllib.quote("customer")
        print request.session['type']
        request.session.modified = True
        if request.session['type'] == "superadmin":
            return HttpResponse(str(1))
        elif request.session['type'] == "departmentadmin":
            return HttpResponse(str(4))
        elif request.session['type'] == "customer":
            return HttpResponse(str(3))
        elif request.session['type'] == "employee":
            return HttpResponse(str(2))
        else:
            return HttpResponse(str(0))
    else:
        tpl = tpl_lookup.get_template("login.html")
        return HttpResponse(tpl.render(uname="",password="",msg = "Incorrect username or password.",pmsg="",unamemsg=""))

def userdashboard(request):
    try:
        s = Session.objects.get(pk=request.session.session_key)
    except:
        return HttpResponseRedirect('/')
    c = request.COOKIES.get('csrftoken','')
    tpl = tpl_lookup.get_template("usrsummry.html")
    user = Alfreduser.objects.all()
    status = TicketStatus.objects.all()
    return HttpResponse(tpl.render(csrf_token=c,on_home=True,status=status,User=user,userName=s.get_decoded()['myname']))

def adduserform(request):
    try:
        s = Session.objects.get(pk=request.session.session_key)
    except:
        return HttpResponseRedirect('/')
    c = request.COOKIES.get('csrftoken','')
    tpl = tpl_lookup.get_template("usr_add.html")
    user = Alfreduser.objects.all()
    status = TicketStatus.objects.all()
    return HttpResponse(tpl.render(csrf_token=c,on_home=True,status=status,User=user,userName='Smita'))

def useradd(request):
    try:
        s = Session.objects.get(pk=request.session.session_key)
    except:
        return HttpResponseRedirect('/')
    ts = datetime.datetime.now()
    username = request.POST.get('username')
    password = request.POST.get('password')
    usertype = request.POST.get('usertype')
    userobj = Alfreduser(Username=username,Password=password,Datejoined=ts,Usertype=usertype)
    userobj.save()

def usereditform(request):
    try:
        s = Session.objects.get(pk=request.session.session_key)
    except:
        return HttpResponseRedirect('/')
    c = request.COOKIES.get('csrftoken','')
    tpl = tpl_lookup.get_template("edituser.html")
    user = Alfreduser.objects.all()
    status = TicketStatus.objects.all()
    return HttpResponse(tpl.render(csrf_token=c,on_home=True,status=status,User=user,userName=s.get_decoded()['myname']))

def modifyuser(request):
    pass 

def deleteuser(request):
    pass

def teamdashboard(request):
    try:
        s = Session.objects.get(pk=request.session.session_key)
    except:
        return HttpResponseRedirect('/')
    c = request.COOKIES.get('csrftoken','')
    tpl = tpl_lookup.get_template("teamsummary.html")
    team = Team.objects.all()
    status = TicketStatus.objects.all()
    return HttpResponse(tpl.render(csrf_token=c,on_home=True,status=status,team=team,userName=s.get_decoded()['myname']))

def dashboard(request):
    try:
        s = Session.objects.get(pk=request.session.session_key)
    except:
        return HttpResponseRedirect('/')
    c = request.COOKIES.get('csrftoken','')
    tpl = tpl_lookup.get_template("dashboard.html")
    team = Team.objects.all()
    status = TicketStatus.objects.all()
    return HttpResponse(tpl.render(csrf_token=c,on_home=True,status=status,team=team,userName=s.get_decoded()['myname']))

def addteamform(request):
    try:
        s = Session.objects.get(pk=request.session.session_key)
    except:
        return HttpResponseRedirect('/')
    c = request.COOKIES.get('csrftoken','')
    tpl = tpl_lookup.get_template("createteam.html")
    dept = Department.objects.all()
    user = []#Alfreduser.objects.all()
    status = TicketStatus.objects.all()
    return HttpResponse(tpl.render(csrf_token=c,on_home=True,dept=dept,status=status,User=user,userName=s.get_decoded()['myname']))

@csrf_exempt
def teamadd(request):
    try:
        s = Session.objects.get(pk=request.session.session_key)
    except:
        return HttpResponseRedirect('/')
    try:
        name = request.POST.get('name')
    except:
        name = None
    try:
        password=request.POST.get('password')
    except:
        password = None
    try:
        address = request.POST.get('address')
    except:
        address = None
    try:
        landline = request.POST.get('landline')
    except:
        landline = None
    try:
        mobile = request.POST.get('mobile')
    except:
        mobile = None
    try:
        email = request.POST.get('email')
    except:
        email = None
    try:
        username = request.POST.get('username')
    except:
        username = None
    try:
        password = request.POST.get('password')
    except:
        password =None
    try:
        usertype = request.POST.get('usertype')
    except:
        usertype = None
    try:
        dept = request.POST.get('dept')
    except:
        dept =None
    deptobj = Department.objects.filter(id=dept)[0]
    try:
        teamobj = Team(username=username,password=password,name=name,address=address,landlineno=landline,mobileno=mobile,email=email,department=deptobj,usertype=usertype)
        teamobj.save()
        return HttpResponse(str(1)) 
    except:
        return HttpResponse(str(0))

@csrf_exempt
def teameditform(request):
    try:
        s = Session.objects.get(pk=request.session.session_key)
    except:
        return HttpResponseRedirect('/')
    c = request.COOKIES.get('csrftoken','')
    tpl = tpl_lookup.get_template("editteam.html")
    teamid = request.GET.get('teamId')
    team = Team.objects.filter(id=teamid)
    dept = Department.objects.all()
    status = TicketStatus.objects.all()
    return HttpResponse(tpl.render(csrf_token=c,on_home=True,issue=dept,team=team[0],status=status,userName=s.get_decoded()['myname']))

@csrf_exempt
def modifyteam(request):
    c = request.COOKIES.get('csrftoken','')
    try:
        s = Session.objects.get(pk=request.session.session_key)
    except:
        return HttpResponseRedirect('/')
    teamid = request.POST.get('memberid')
    name = request.POST.get('membername')
    address = request.POST.get('teamaddress')
    landlineno = request.POST.get('landline')
    mobileno = request.POST.get('mobile')
    email = request.POST.get('email')
    username = request.POST.get('username')
    password = request.POST.get('password')
    role  = request.POST.get('role')
    dept = request.POST.get('dept')
    deptobj = Department.objects.filter(id=dept)[0]
    try:
        obj = Team.objects.filter(id=teamid).update(name=name,address=address,landlineno=landlineno,mobileno=mobileno,email=email,department=deptobj,usertype=role)
        return HttpResponse(str(1))
    except:
        return HttpResponse(str(0))

@csrf_exempt
def deleteteam(request):
    c = request.COOKIES.get('csrftoken','')
    try:
        s = Session.objects.get(pk=request.session.session_key)
    except:
        return HttpResponseRedirect('/')
    teamid = request.POST.get('memberid')
    try:
        Team.objects.filter(id=teamid).delete()
        return HttpResponse(str(1))
    except:
        return HttpResponse(str(0))

def employeedashboard(request):
    c = request.COOKIES.get('csrftoken','')
    try:
        s = Session.objects.get(pk=request.session.session_key)
    except:
        return HttpResponseRedirect('/')
    username = s.get_decoded()['myname']
    teamobj = Team.objects.filter(username = username)
    tkobjlist = getTicketByAssignedUser(teamobj)
    tkobjlist.reverse()
    tpl = tpl_lookup.get_template("employeesummary.html")
    status = TicketStatus.objects.all()
    return HttpResponse(tpl.render(csrf_token=c,on_home=True,status=status,ticket=tkobjlist,userName=s.get_decoded()['myname']))



    
def departmentdashboard(request):
    try:
        s = Session.objects.get(pk=request.session.session_key)
    except:
        return HttpResponseRedirect('/')
    c = request.COOKIES.get('csrftoken','')
    tpl = tpl_lookup.get_template("issuemaster.html")
    status = TicketStatus.objects.all()
    department = Department.objects.all() 
    return HttpResponse(tpl.render(csrf_token=c,on_home=True,status=status,department=department,userName=s.get_decoded()['myname']))

@csrf_exempt
def departmentadd(request):
    try:
        s = Session.objects.get(pk=request.session.session_key)
    except:
        return HttpResponseRedirect('/')
    c = request.COOKIES.get('csrftoken','')
    department = request.POST.get('department')
    newdepartment = department.title()
    try:
        deptobj = Department(department=newdepartment)
        deptobj.save()
        return HttpResponse(str(1))
    except:
        return HttpResponse(str(0))

def departmentedit(request):
    try:
        s = Session.objects.get(pk=request.session.session_key)
    except:
        return HttpResponseRedirect('/')
    c = request.COOKIES.get('csrftoken','')
    deptid = request.GET.get('deptid')
    try:
        deptobj = Department.objects.filter(id=deptid)
    except:
        deptobj = None
    tpl = tpl_lookup.get_template("editissuemaster.html")
    status = TicketStatus.objects.all()
    return HttpResponse(tpl.render(csrf_token=c,on_home=True,status=status,dept=deptobj[0],userName=s.get_decoded()['myname']))

@csrf_exempt
def departmentmodify(request):
    try:
        s = Session.objects.get(pk=request.session.session_key)
    except:
        return HttpResponseRedirect('/')
    c = request.COOKIES.get('csrftoken','')
    deptid = request.POST.get('deptid')
    dept = request.POST.get('dept')
    newdept = dept.title()
    obj = Department.objects.filter(id=deptid).update(department=newdept)
    return HttpResponse(str(obj))

@csrf_exempt
def deletedepartment(request):
    try:
        s = Session.objects.get(pk=request.session.session_key)
    except:
        return HttpResponseRedirect('/')
    c = request.COOKIES.get('csrftoken','')
    deptid = request.POST.get('deptid')
    try:
        obj = Department.objects.filter(id=deptid).delete()
        return HttpResponse(str(1))
    except:
        return HttpResponse(str(0))

def customerpackagedashboard(request):
    try:
        s = Session.objects.get(pk=request.session.session_key)
    except:
        return HttpResponseRedirect('/')
    c = request.COOKIES.get('csrftoken','')
    tpl = tpl_lookup.get_template("customerpackage.html")
    status = TicketStatus.objects.all()
    customerpackage = CustomerPackage.objects.all() 
    return HttpResponse(tpl.render(csrf_token=c,on_home=True,status=status,customerpackage=customerpackage,userName=s.get_decoded()['myname']))

@csrf_exempt
def customerpackageadd(request):
    try:
        s = Session.objects.get(pk=request.session.session_key)
    except:
        return HttpResponseRedirect('/')
    c = request.COOKIES.get('csrftoken','')
    customerpackage = request.POST.get('customer_package')
    newcustomerpackage = customerpackage.title()
    try:
        deptobj = CustomerPackage(package_type=newcustomerpackage)
        deptobj.save() 
        return HttpResponse(str(1))
    except:
        return HttpResponse(str(0))

def customerpackageedit(request):
    try:
        s = Session.objects.get(pk=request.session.session_key)
    except:
        return HttpResponseRedirect('/')
    c = request.COOKIES.get('csrftoken','')
    packageid = request.GET.get('packageid')
    try:
        custpkgobj = CustomerPackage.objects.filter(id=packageid)
    except:
        custpkgobj = None
    tpl = tpl_lookup.get_template("editcustomerpackage.html")
    status = TicketStatus.objects.all()
    return HttpResponse(tpl.render(csrf_token=c,on_home=True,status=status,custpkg=custpkgobj[0],userName=s.get_decoded()['myname']))

@csrf_exempt
def customerpackagemodify(request):
    try:
        s = Session.objects.get(pk=request.session.session_key)
    except:
        return HttpResponseRedirect('/')
    c = request.COOKIES.get('csrftoken','')
    packageid = request.POST.get('packageid')
    packagetype = request.POST.get('packagetype')
    newpackagetype = packagetype.title()
    try:
        custpkgobj = CustomerPackage.objects.filter(id=packageid).update(package_type=newpackagetype)
        return HttpResponse(str(1))
    except:
        custpkgobj = None
        return HttpResponse(str(0))

@csrf_exempt
def customerpackagedelete(request):
    try:
        s = Session.objects.get(pk=request.session.session_key)
    except:
        return HttpResponseRedirect('/')
    c = request.COOKIES.get('csrftoken','')
    customerpackageid = request.POST.get('customerpackageid')
    try:
        obj = CustomerPackage.objects.filter(id=customerpackageid).delete()
        return HttpResponse(str(1))
    except:
        return HttpResponse(str(0))

def sladashboard(request):
    try:
        s = Session.objects.get(pk=request.session.session_key)
    except:
        return HttpResponseRedirect('/')
    c = request.COOKIES.get('csrftoken','')
    tpl = tpl_lookup.get_template("slatype.html")
    status = TicketStatus.objects.all()
    sla = Sla.objects.all() 
    return HttpResponse(tpl.render(csrf_token=c,on_home=True,status=status,sla=sla,userName=s.get_decoded()['myname']))

@csrf_exempt
def slaadd(request):
    try:
        s = Session.objects.get(pk=request.session.session_key)
    except:
        return HttpResponseRedirect('/')
    c = request.COOKIES.get('csrftoken','')
    sla = request.POST.get('sla_type')
    newsla = sla.title()
    try:      
        slaobj = Sla(slatype=newsla)
        slaobj.save()
        return HttpResponse(str(1))
    except:
        return HttpResponse(str(0))

def slaedit(request):
    try:
        s = Session.objects.get(pk=request.session.session_key)
    except:
        return HttpResponseRedirect('/')
    c = request.COOKIES.get('csrftoken','')
    slaid = request.GET.get('slaid')
    try:
        slaobj = Sla.objects.filter(id=slaid)
    except:
        slaobj = None
    tpl = tpl_lookup.get_template("editslatype.html")
    status = TicketStatus.objects.all()
    return HttpResponse(tpl.render(csrf_token=c,on_home=True,status=status,slaobj=slaobj[0],userName=s.get_decoded()['myname']))

@csrf_exempt
def slamodify(request):
    try:
        s = Session.objects.get(pk=request.session.session_key)
    except:
        return HttpResponseRedirect('/')
    c = request.COOKIES.get('csrftoken','')
    slaid = request.POST.get('slaid')
    slatype = request.POST.get('slatype')
    newslatype = slatype.title()
    try:
        custpkgobj = Sla.objects.filter(id=slaid).update(slatype=newslatype)
        return HttpResponse(str(1))
    except:
        custpkgobj = None
    return HttpResponse(str(0))

@csrf_exempt
def sladelete(request):
    try:
        s = Session.objects.get(pk=request.session.session_key)
    except:
        return HttpResponseRedirect('/')
    c = request.COOKIES.get('csrftoken','')
    slaid = request.POST.get('slaid')
    try:
        obj = Sla.objects.filter(id=slaid).delete()
        return HttpResponse(str(1))
    except:
        return HttpResponse(str(0))

def ticketstatusdashboard(request):
    try:
        s = Session.objects.get(pk=request.session.session_key)
    except:
        return HttpResponseRedirect('/')
    c = request.COOKIES.get('csrftoken','')
    tpl = tpl_lookup.get_template("ticketstatusmaster.html")
    status = TicketStatus.objects.all()
    return HttpResponse(tpl.render(csrf_token=c,on_home=True,ticket=status,status=status,userName=s.get_decoded()['myname']))

@csrf_exempt
def ticketstatusadd(request):
    try:
        s = Session.objects.get(pk=request.session.session_key)
    except:
        return HttpResponseRedirect('/')
    c = request.COOKIES.get('csrftoken','')
    statustype = request.POST.get('ticket_status')
    newstatustype = statustype.title()
    try:      
        ticketstatusobj = TicketStatus(statustype=newstatustype)
        ticketstatusobj.save() 
        return HttpResponse(str(1))
    except:
        return HttpResponse(str(0))

@csrf_exempt
def ticketstatusedit(request):
    try:
        s = Session.objects.get(pk=request.session.session_key)
    except:
        return HttpResponseRedirect('/')
    c = request.COOKIES.get('csrftoken','')
    statusId = request.GET.get('statusId')
    try:
        statusobj = TicketStatus.objects.filter(id=statusId)
    except:
        statusobj = None
    tpl = tpl_lookup.get_template("editticketstatus.html")
    status = TicketStatus.objects.all()
    return HttpResponse(tpl.render(csrf_token=c,on_home=True,status=status,statusobj=statusobj[0],userName=s.get_decoded()['myname']))

@csrf_exempt
def ticketstatusmodify(request):
    try:
        s = Session.objects.get(pk=request.session.session_key)
    except:
        return HttpResponseRedirect('/')
    c = request.COOKIES.get('csrftoken','')
    statusId = request.POST.get('statusId')
    statustype = request.POST.get('statustype')
    newstatustype = statustype.title()
    try:
        custpkgobj = TicketStatus.objects.filter(id=statusId).update(statustype=newstatustype)
        return HttpResponse(str(1))
    except:
        custpkgobj = None
    return HttpResponse(str(0))

@csrf_exempt
def ticketstatusdelete(request):
    try:
        s = Session.objects.get(pk=request.session.session_key)
    except:
        return HttpResponseRedirect('/')
    c = request.COOKIES.get('csrftoken','')
    statusId = request.POST.get('statusId')
    try:
        obj = TicketStatus.objects.filter(id=statusId).delete()
        return HttpResponse(str(1))
    except:
        return HttpResponse(str(0))

def customersummary(request):
    try:
        s = Session.objects.get(pk=request.session.session_key)
    except:
        return HttpResponseRedirect('/')
    c = request.COOKIES.get('csrftoken','')
    tpl = tpl_lookup.get_template("customersummary.html")
    customer = Customer.objects.all()
    user = Alfreduser.objects.all()
    status = TicketStatus.objects.all()
    return HttpResponse(tpl.render(csrf_token=c,on_home=True,customer=customer,status=status,User=user,userName=s.get_decoded()['myname']))

@csrf_exempt
def modifydepartment(request):
    try:
        s = Session.objects.get(pk=request.session.session_key)
    except:
        return HttpResponseRedirect('/')
    c = request.COOKIES.get('csrftoken','')
    deptid = request.POST.get('deptid')
    dept = request.POST.get('dept')
    obj = Department.objects.filter(id=deptid).update(department=dept)
    return HttpResponse(str(obj))


@csrf_exempt
def customerdashboard(request):
    s = None
    try:
        s = Session.objects.get(pk=request.session.session_key)
    except:
        return HttpResponseRedirect('/')
    c = request.COOKIES.get('csrftoken','')
    ticketList = []
    tpl = tpl_lookup.get_template("customer_ticket_summary.html")
    username = s.get_decoded()['myname']
    customer = Customer.objects.filter(username=username)[0]
    allTicket = getAllTicketByCust(customer)    
    allTicket.reverse()
    status = TicketStatus.objects.all()  
    return HttpResponse(tpl.render(csrf_token=c,on_home=True,customer=customer,status=status,ticket=allTicket,userName=s.get_decoded()['myname']))

@csrf_exempt
def customerdisplayticketBystatus(request):
    s = None
    try:
        s = Session.objects.get(pk=request.session.session_key)
    except:
        return HttpResponseRedirect('/')
    c = request.COOKIES.get('csrftoken','')
    status = request.GET.get('status')
    username = s.get_decoded()['myname']
    customer = Customer.objects.filter(username=username)[0]
    ticketdata = getTicketBystatusandcust(status,customer.id)
    tpl = tpl_lookup.get_template("displayticketstatuswise.html")
    status = TicketStatus.objects.all()  
    return HttpResponse(tpl.render(csrf_token=c,on_home=True,ticket=ticketdata,status=status,userName=s.get_decoded()['myname']))

@csrf_exempt
def teamdisplayticketBystatus(request):
    s = None
    try:
        s = Session.objects.get(pk=request.session.session_key)
    except:
        return HttpResponseRedirect('/')
    c = request.COOKIES.get('csrftoken','')
    status = request.GET.get('status')
    username = s.get_decoded()['myname']
    team = Team.objects.filter(username=username)[0]
    try:
        ticketdata = getAllTicketByStatusAndDept(status,team.department.id)
    except:
        ticketdata = []
    tpl = tpl_lookup.get_template("undeobs_ticket.html")
    status = TicketStatus.objects.all()  
    return HttpResponse(tpl.render(csrf_token=c,on_home=True,ticket=ticketdata,status=status,userName=s.get_decoded()['myname']))

@csrf_exempt
def teamadmindashboard(request):
    s = None
    try:
        s = Session.objects.get(pk=request.session.session_key)
    except:
        return HttpResponseRedirect('/')
    c = request.COOKIES.get('csrftoken','')
    department = s.get_decoded()['department']
    username = s.get_decoded()['myname']
    team = Team.objects.filter(username=username)[0]
    tpl = tpl_lookup.get_template("admin_ticket_assign.html")
    ticketData = []
    ticketData = getAllTicketByDept(team.department.department)        
    ticketData.reverse()
    status = TicketStatus.objects.all()  
    return HttpResponse(tpl.render(csrf_token=c,on_home=True,ticket=ticketData,status=status,assign=Team.objects.all(),userName=s.get_decoded()['myname']))
#        

def customeradd(request):
    try:
        s = Session.objects.get(pk=request.session.session_key)
    except:
        return HttpResponseRedirect('/')
    c = request.COOKIES.get('csrftoken','')
    tpl = tpl_lookup.get_template("createcustomer.html")
    user = Alfreduser.objects.all()
    status = TicketStatus.objects.all()
    return HttpResponse(tpl.render(csrf_token=c,on_home=True,status=status,User=user,userName=s.get_decoded()['myname']))

#def editcustomer(request):
#    try:
#        s = Session.objects.get(pk=request.session.session_key)
#    except:
#        return HttpResponseRedirect('/')
#    c = request.COOKIES.get('csrftoken','')
#    custid = request.GET.get('teamId')
#    cust = CustomerPackage.objects.filter(id=slaid)
#    tpl = tpl_lookup.get_template("editcustomer.html")
#    status = TicketStatus.objects.all()
#    return HttpResponse(tpl.render(csrf_token=c,on_home=True,team=team,status=status,User=user,userName=s.get_decoded()['myname']))

@csrf_exempt
def customeraddpost(request):
    try:
        s = Session.objects.get(pk=request.session.session_key)
    except:
        return HttpResponseRedirect('/')
    try:
        customer_name = request.POST.get('customer_name')
    except:
        customer_name = None
    try:
        company_name = request.POST.get('company_name')
    except:
        company_name = None
    try:
        email = request.POST.get('email')
    except:
        email = None
    try:
        location = request.POST.get('location')
    except:
        location = None
    try:
        mobile = request.POST.get('mobile')
    except:
        mobile = None
    try:
        landline = request.POST.get('landline')
    except:
        landline = None
    try:
        username = request.POST.get('username')
    except:
        username = None
    try:
        password = request.POST.get('password')
    except:
        password =None
    try:
        custobj = Customer(username=username,password=password,email=email,name=customer_name,company=company_name,address=location,mobile=mobile,landline=landline)
        custobj.save()
        return HttpResponse(str(1))
    except:
        return HttpResponse(str(0))

@csrf_exempt
def customeredit(request):
    try:
        s = Session.objects.get(pk=request.session.session_key)
    except:
        return HttpResponseRedirect('/')
    c = request.COOKIES.get('csrftoken','')
    custId = request.GET.get('custId')
    customer = Customer.objects.filter(id=custId)[0]
    c = request.COOKIES.get('csrftoken','')
    tpl = tpl_lookup.get_template("editcustomer.html")
    status = TicketStatus.objects.all()
    return HttpResponse(tpl.render(csrf_token=c,on_home=True,customer=customer,status=status,userName=s.get_decoded()['myname'])) 

@csrf_exempt
def customermodify(request):
    try:
        s = Session.objects.get(pk=request.session.session_key)
    except:
        return HttpResponseRedirect('/')
    try:
        custId = request.POST.get('customer_id')
    except:
        custId = None
    try:
        customer_name = request.POST.get('customer_name')
    except:
        customer_name = None
    try:
        company_name = request.POST.get('company_name')
    except:
        company_name = None
    try:
        email = request.POST.get('email')
    except:
        email = None
    try:
        location = request.POST.get('location')
    except:
        location = None
    try:
        mobile = request.POST.get('mobile')
    except:
        mobile = None
    try:
        landline = request.POST.get('landline')
    except:
        landline = None
    try:
        username = request.POST.get('username')
    except:
        username = None
    try:
        password = request.POST.get('password')
    except:
        password =None
    obj = Customer.objects.filter(id=custId).update(name=customer_name,company=company_name,email=email,address=location,mobile=mobile,landline=landline,password=password)
    return HttpResponse(str(obj))

@csrf_exempt
def deletecustomer(request):
    try:
        s = Session.objects.get(pk=request.session.session_key)
    except:
        return HttpResponseRedirect('/')
    c = request.COOKIES.get('csrftoken','')
    custId = request.POST.get('custId')
    obj = Customer.objects.filter(id=custId).delete()
    return HttpResponse(str(1))

@csrf_exempt
def createcustomerTicketform(request):
    s = None
    try:
        s = Session.objects.get(pk=request.session.session_key)
    except:
        return HttpResponseRedirect('/')
    c = request.COOKIES.get('csrftoken','')
    username = s.get_decoded()['myname']
    customerobj = Customer.objects.filter(username = username)    
    tpl = tpl_lookup.get_template("ticket.html")
    
    status = TicketStatus.objects.all()
    department = Department.objects.all()
    make = Make.objects.all()
    #data = {"customer":customerobj,"statusList":statusList,"issue":Issue.getAllIssueType(),"make":Make.getAllmakeType(),"userName":urllib.unquote(cookieuserName)}
    return HttpResponse(tpl.render(csrf_token=c,on_home=True,customer=customerobj[0],status=status,department=department,make=make,userName=s.get_decoded()['myname']))

@csrf_exempt
def createcustomerTicket(request):
    try:
        s = Session.objects.get(pk=request.session.session_key)
    except:
        return HttpResponseRedirect('/')
    date = datetime.datetime.now()
    try:
        custId = request.POST.get('custid')
    except:
        custId = None
    try:
        system_id =request.POST.get('system_id')
    except:
        system_id = None
    try:
        problem = request.POST.get('problem')
    except:
        problem = None
    try:
        dept=request.POST.get("issue_type")
    except:
        dept = None
    try:
        attachment = request.POST.get("files")
    except:
        attachment = None
    ticketid ="PSSPL/"+strftime("%y/%m/%d/%H/%M/%S")    
    customerobj = Customer.objects.filter(id=custId)[0]
    deptobj = Department.objects.filter(id=dept)[0] 
    ticketobj = Ticket.objects.create(ts=date,ticketid=ticketid,customer=customerobj,dept=deptobj,systemid=system_id,summary=problem,attachment=attachment)
    ticketobj.save()
    return HttpResponse(str(1))

@csrf_exempt
def createteamTicketform(request):
    s = None
    try:
        s = Session.objects.get(pk=request.session.session_key)
    except:
        return HttpResponseRedirect('/')
    c = request.COOKIES.get('csrftoken','')
    status = TicketStatus.objects.all()
    department = Department.objects.all()
    make = Make.objects.all()    
    custdata = Customer.objects.all()
    tpl = tpl_lookup.get_template("dept_create_ticket.html")
    #data = {"customerdata":custobj,"status":TicketStatus.getAllTicketStatus(),"statusList":statusList,"issue":Issue.getAllIssueType(),"make":Make.getAllmakeType(),"userName":urllib.unquote(cookieuserName),"usertype":urllib.unquote(cookieuserType),"tkStatus":TicketStatus.getAllTicketStatus()}
    return HttpResponse(tpl.render(csrf_token=c,on_home=True,customerdata=custdata,status=status,department=department,make=make,userName=s.get_decoded()['myname']))

@csrf_exempt
def createteamTicket(request):
    try:
        s = Session.objects.get(pk=request.session.session_key)
    except:
        return HttpResponseRedirect('/')
    date = datetime.datetime.now()
    c = request.COOKIES.get('csrftoken','')
    try:
        custId = request.POST.get('customer')
    except:
        custId = None
    try:
        system_id =request.POST.get('system_id')
    except:
        system_id = None
    try:
        problem = request.POST.get('problem')
    except:
        problem = None
    try:
        dept=request.POST.get("issue_type")
    except:
        dept = None
    try:
        attachment = request.POST.get("files")
    except:
        attachment = None
    ticketid ="PSSPL/"+strftime("%y/%m/%d/%H/%M/%S")    
    customerobj = Customer.objects.filter(id=custId)[0]
    deptobj = Department.objects.filter(id=dept)[0] 
    ticketobj = Ticket.objects.create(ts=date,ticketid=ticketid,customer=customerobj,dept=deptobj,systemid=system_id,summary=problem,attachment=attachment)
    ticketobj.save()
    return HttpResponse(str(1))

def createemployeeTicketform(request):
    s = None
    try:
        s = Session.objects.get(pk=request.session.session_key)
    except:
        return HttpResponseRedirect('/')
    c = request.COOKIES.get('csrftoken','')
    status = TicketStatus.objects.all()
    department = Department.objects.all()
    make = Make.objects.all()    
    custdata = Customer.objects.all()
    tpl = tpl_lookup.get_template("dept_create_ticket.html")
    #data = {"customerdata":custobj,"status":TicketStatus.getAllTicketStatus(),"statusList":statusList,"issue":Issue.getAllIssueType(),"make":Make.getAllmakeType(),"userName":urllib.unquote(cookieuserName),"usertype":urllib.unquote(cookieuserType),"tkStatus":TicketStatus.getAllTicketStatus()}
    return HttpResponse(tpl.render(csrf_token=c,on_home=True,customerdata=custdata,status=status,department=department,make=make,userName=s.get_decoded()['myname']))



def createticketform(request):
    try:
        s = Session.objects.get(pk=request.session.session_key)
    except:
        return HttpResponseRedirect('/')
    c = request.COOKIES.get('csrftoken','')
    tpl = tpl_lookup.get_template("sadmin_create_ticket.html")
    customer = Customer.objects.all()
    department = Department.objects.all()
    user = Alfreduser.objects.all()
    status = TicketStatus.objects.all()
    return HttpResponse(tpl.render(csrf_token=c,on_home=True,department=department,customer=customer,status=status,User=user,userName=s.get_decoded()['myname']))

@csrf_exempt
def createticket(request):
    try:
        s = Session.objects.get(pk=request.session.session_key)
    except:
        return HttpResponseRedirect('/')
    date = datetime.datetime.now()
    try:
        custId = request.POST.get('customer')
    except:
        custId = None
    try:
        system_id =request.POST.get('system_id')
    except:
        system_id = None
    try:
        problem = request.POST.get('problem')
    except:
        problem = None
    try:
        dept=request.POST.get("issue_type")
    except:
        dept = None
    try:
        attachment = request.POST.get("files")
    except:
        attachment = None
    ticketid ="PSSPL/"+strftime("%y/%m/%d/%H/%M/%S")    
    customerobj = Customer.objects.filter(id=custId)[0]
    deptobj = Department.objects.filter(id=dept)[0] 
    ticketobj = Ticket.objects.create(ts=date,ticketid=ticketid,customer=customerobj,dept=deptobj,systemid=system_id,summary=problem,attachment=attachment)
    ticketobj.save()
    c = request.COOKIES.get('csrftoken','')
    tpl = tpl_lookup.get_template("sadmin_create_ticket.html")
    customer = Customer.objects.all()
    department = Department.objects.all()
    user = Alfreduser.objects.all()
    status = TicketStatus.objects.all()
    return HttpResponse(tpl.render(csrf_token=c,on_home=True,department=department,customer=customer,status=status,User=user,userName=s.get_decoded()['myname']))

@csrf_exempt
def dispcustomerdata(request):
    try:
        s = Session.objects.get(pk=request.session.session_key)
    except:
        return HttpResponseRedirect('/')
    c = request.COOKIES.get('csrftoken','')
    custId = request.POST.get('customerid')
    obj = Customer.objects.filter(id=custId)
    listdata = []
    for i in obj:
        listdata.append((i.name,i.company,i.address,i.landline,i.mobile,i.email))
    dict = {"data":listdata[0]}
    return HttpResponse(json.dumps(dict))
    return HttpResponse(tpl.render(csrf_token=c,on_home=True,customer=customer,status=status,User=user,userName=s.get_decoded()['myname']))

def ticketreports(request):
    try:
        s = Session.objects.get(pk=request.session.session_key)
    except:
        return HttpResponseRedirect('/')
    c = request.COOKIES.get('csrftoken','')
    tpl = tpl_lookup.get_template("report.html")
    user = Alfreduser.objects.all()
    status = TicketStatus.objects.all()
    return HttpResponse(tpl.render(csrf_token=c,on_home=True,status=status,User=user,userName=s.get_decoded()['myname'],date=strftime("%Y/%m/%d")))

def ticketreportscustomer(request):
    try:
        s = Session.objects.get(pk=request.session.session_key)
    except:
        return HttpResponseRedirect('/')
    c = request.COOKIES.get('csrftoken','')
    tpl = tpl_lookup.get_template("customerreport.html")
    user = Alfreduser.objects.all()
    status = TicketStatus.objects.all()
    return HttpResponse(tpl.render(csrf_token=c,on_home=True,status=status,User=user,userName=s.get_decoded()['myname'],date=strftime("%Y/%m/%d")))

def ticketreportsfeedback(request):
    try:
        s = Session.objects.get(pk=request.session.session_key)
    except:
        return HttpResponseRedirect('/')
    
def ticketAssign(request):
    try:
        s = Session.objects.get(pk=request.session.session_key)
    except:
        return HttpResponseRedirect('/')
    c = request.COOKIES.get('csrftoken','')
    tpl = tpl_lookup.get_template("ticket_assign.html")
    ticket = []
    for i in Ticket.objects.all():
        ticket.append(i)
    ticket.reverse()
    status = TicketStatus.objects.all()
    status = TicketStatus.objects.all()
    return HttpResponse(tpl.render(csrf_token=c,on_home=True,status=status,userName=s.get_decoded()['myname'],ticket=ticket[0:20],first=0,last=20,count=len(ticket)))

