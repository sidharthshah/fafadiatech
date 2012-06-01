import os
import urllib
import datetime
from time import gmtime, strftime
from dateutil.relativedelta import *
from dateutil.rrule import *
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




def home(request):
    try:
        s = Session.objects.get(pk=request.session.session_key)
        s.delete()
        c = request.COOKIES.get('csrftoken','')
        tpl = tpl_lookup.get_template("login.html")
        user = Alfreduser.objects.all()
        statusobj = TicketStatus()    
        status = statusobj.getallticketstatus()
        return HttpResponse(tpl.render(csrf_token=c,on_home=True,uname="status",password="user",unamemsg="dfdfdf",pmsg="",msg="",userName='Smita'))
    except:
        c = request.COOKIES.get('csrftoken','')
        tpl = tpl_lookup.get_template("login.html")
        user = Alfreduser.objects.all()
        statusobj = TicketStatus()    
        status = statusobj.getallticketstatus()
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
            request.session['department'] = urllib.quote(str(userobj.department.id))
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
    statusobj = TicketStatus()    
    status = statusobj.getallticketstatus()
    return HttpResponse(tpl.render(csrf_token=c,on_home=True,status=status,User=user,userName=s.get_decoded()['myname']))

def adduserform(request):
    try:
        s = Session.objects.get(pk=request.session.session_key)
    except:
        return HttpResponseRedirect('/')
    c = request.COOKIES.get('csrftoken','')
    tpl = tpl_lookup.get_template("usr_add.html")
    user = Alfreduser.objects.all()
    statusobj = TicketStatus()    
    status = statusobj.getallticketstatus()
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
    statusobj = TicketStatus()    
    status = statusobj.getallticketstatus()
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
    teamobj = Team()    
    team = teamobj.getallteam()
    statusobj = TicketStatus()    
    status = statusobj.getallticketstatus()
    return HttpResponse(tpl.render(csrf_token=c,on_home=True,status=status,team=team,userName=s.get_decoded()['myname']))

def dashboard(request):
    try:
        s = Session.objects.get(pk=request.session.session_key)
    except:
        return HttpResponseRedirect('/')
    allday = []
    now = datetime.datetime.now()
    lastweekdate = now+relativedelta(weeks=-1)
    lastweekdates = list(rrule(DAILY,dtstart=lastweekdate,until=now))
    tkobj = Ticket()
    for i in lastweekdates:
            allday.append(len(tkobj.getdatewiseticket(i)))
    allday = allday[1:]
    
    statusobj = TicketStatus()    
    status = statusobj.getallticketstatus()
      
    weeklyTicket = []
    dict = {}
    for j in lastweekdates:
        data = {}
        tkobj = Ticket()
        for k in tkobj.getdatewiseticket(j):
            for l in status:
                count = 0
                try:
                    if k.status.statustype == l.statustype:
                        count = count+1
                except:
                    pass
                if data.has_key(l.statustype):
                    data[l.statustype] = data[l.statustype] + count
                else:
                    data[l.statustype] = count
        weeklyTicket.append(data)
    
    datatolist = []
    for key in status:
        info = []
        for dict in weeklyTicket[1:8]: 
           try:
               info.append(dict[key.statustype])
           except:
              info.append(0)
        datatolist.append({"name":str(key.statustype),"data":info})
        
        
    dictdata = {}
    
    
    for sts in status:
        tkobj = Ticket()
        statuscount = 0
        for ticket in tkobj.getallticket():
            try:
                if ticket.status.statustype == sts.statustype:
                    statuscount = statuscount + 1
            except:
                pass
            dictdata[sts.statustype]= statuscount            
    newdata = []
    for key, value in dictdata.items():
        newdata.append([str(key),value])
    c = request.COOKIES.get('csrftoken','')
    tpl = tpl_lookup.get_template("dashboard.html")
    teamobj = Team()    
    team = teamobj.getallteam()
    return HttpResponse(tpl.render(csrf_token=c,on_home=True,status=status,team=team,userName=s.get_decoded()['myname'],allday=allday,weklydata=weeklyTicket[0:7],datatolist=datatolist,newdata=newdata))

def addteamform(request):
    try:
        s = Session.objects.get(pk=request.session.session_key)
    except:
        return HttpResponseRedirect('/')
    c = request.COOKIES.get('csrftoken','')
    tpl = tpl_lookup.get_template("createteam.html")
    deptobj = Department()
    dept = deptobj.getalldept()
    user = []#Alfreduser.objects.all()
    statusobj = TicketStatus()    
    status = statusobj.getallticketstatus()
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
    obj = Department()
    deptobj = obj.getdepartmentbyid(dept)
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
    teamobj = Team()
    team = teamobj.getteammemberbyid(teamid)
    deptobj = Department()
    dept = deptobj.getalldept()
    statusobj = TicketStatus()    
    status = statusobj.getallticketstatus()
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
    obj = Department()
    deptobj = obj.getdepartmentbyid(dept)
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
    username = s.get_decoded()['userid']
    tkobj = Ticket()
    tkobjlist = tkobj.getticketbyassigneduser(username)
    tkobjlist.reverse()
    tpl = tpl_lookup.get_template("employeesummary.html")
    statusobj = TicketStatus()    
    status = statusobj.getallticketstatus()
    return HttpResponse(tpl.render(csrf_token=c,on_home=True,status=status,ticket=tkobjlist,userName=s.get_decoded()['myname']))

def departmentdashboard(request):
    try:
        s = Session.objects.get(pk=request.session.session_key)
    except:
        return HttpResponseRedirect('/')
    c = request.COOKIES.get('csrftoken','')
    tpl = tpl_lookup.get_template("issuemaster.html")
    statusobj = TicketStatus()    
    status = statusobj.getallticketstatus()
    deptobj = Department()
    dept = deptobj.getalldept() 
    return HttpResponse(tpl.render(csrf_token=c,on_home=True,status=status,department=dept,userName=s.get_decoded()['myname']))

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
    statusobj = TicketStatus()    
    status = statusobj.getallticketstatus()
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
    statusobj = TicketStatus()    
    status = statusobj.getallticketstatus()
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
    statusobj = TicketStatus()    
    status = statusobj.getallticketstatus()
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
    statusobj = TicketStatus()    
    status = statusobj.getallticketstatus()
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
    statusobj = TicketStatus()    
    status = statusobj.getallticketstatus()
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
    statusobj = TicketStatus()    
    status = statusobj.getallticketstatus()
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
    statusobj = TicketStatus()    
    status = statusobj.getallticketstatus()
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
    custobj = Customer()    
    customer = custobj.getallcustomer()
    user = Alfreduser.objects.all()
    statusobj = TicketStatus()    
    status = statusobj.getallticketstatus()
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
    userid = s.get_decoded()['userid']
    tkobj = Ticket()
    allTicket = tkobj.getallticketbycust(userid)    
    allTicket.reverse()
    statusobj = TicketStatus()    
    status = statusobj.getallticketstatus()
    return HttpResponse(tpl.render(csrf_token=c,on_home=True,status=status,ticket=allTicket,userName=s.get_decoded()['myname']))

@csrf_exempt
def customerdisplayticketbystatus(request):
    s = None
    try:
        s = Session.objects.get(pk=request.session.session_key)
    except:
        return HttpResponseRedirect('/')
    c = request.COOKIES.get('csrftoken','')
    status = request.GET.get('status')
    username = s.get_decoded()['myname']
    customer = Customer.objects.filter(username=username)[0]
    tkobj = Ticket()
    ticketdata = tkobj.getticketbystatusandcust(status,customer.id)
    tpl = tpl_lookup.get_template("displayticketstatuswise.html")
    statusobj = TicketStatus()    
    status = statusobj.getallticketstatus()  
    return HttpResponse(tpl.render(csrf_token=c,on_home=True,ticket=ticketdata,status=status,userName=s.get_decoded()['myname']))

@csrf_exempt
def customerdisplayticket(request):
    s = None
    try:
        s = Session.objects.get(pk=request.session.session_key)
    except:
        return HttpResponseRedirect('/')
    c = request.COOKIES.get('csrftoken','')
    ticketId = request.GET.get("id")
    tpl = tpl_lookup.get_template("reportdetails.html")
    ticketobj = Ticket.objects.filter(id=ticketId)[0]
    c = request.COOKIES.get('csrftoken','')
    tkDict = {}
#    try:
#        tkDict[ticketId]=TicketActivity.getTicketActivityByTicketId(ticketId)
#    except:
#        tkDict[ticketId]=()
    statusobj = TicketStatus()    
    status = statusobj.getallticketstatus()  
    return HttpResponse(tpl.render(csrf_token=c,on_home=True,ticket=ticketobj,statusList=status,status=status,userName=s.get_decoded()['myname']))
            
def employeeallticket(request):
    s = None
    try:
        s = Session.objects.get(pk=request.session.session_key)
    except:
        return HttpResponseRedirect('/')
    c = request.COOKIES.get('csrftoken','')
    username = s.get_decoded()['myname']
    employee = Team.objects.filter(username=username)[0]
    ticketlist = []
    tkobj = Ticket()
    allTicket = tkobj.getallticketbydept(employee.department.id)
    allTicket.reverse()
    statusobj = TicketStatus()    
    status = statusobj.getallticketstatus()
    tpl = tpl_lookup.get_template("employee_alltickets.html")
    return HttpResponse(tpl.render(csrf_token=c,on_home=True,allTicket=allTicket,status=status,tkStatus=status,userName=s.get_decoded()['myname']))

@csrf_exempt
def employeeticketdetails(request):
    s = None
    try:
        s = Session.objects.get(pk=request.session.session_key)
    except:
        return HttpResponseRedirect('/')
    statusobj = TicketStatus()    
    status = statusobj.getallticketstatus()
    c = request.COOKIES.get('csrftoken','')
    username = s.get_decoded()['myname']
    ticketId = request.GET.get("id")
    ticketobj = Ticket.objects.filter(id=ticketId)[0]
    tpl = tpl_lookup.get_template("teamdetails.html")
    tkDict = {}
    try:
        tkDict[ticketId]=TicketActivity.getTicketActivityByTicketId(ticketId)
    except:
        tkDict[ticketId]=()
    #data = {"ticket":ticketobj,"make":make, "customer_pkg":customer_pkg, "sla":sla, "dept":dept, "assign":assign,"tkStatus":TicketStatus.getAllTicketStatus(),"status":tkstatus, "userName":urllib.unquote(cookieuserName),"history":tkDict}
    return HttpResponse(tpl.render(csrf_token=c,on_home=True,ticket=ticketobj,status=status,tkStatus=status,userName=s.get_decoded()['myname']))


@csrf_exempt
def teamdisplayticketbystatus(request):
    s = None
    try:
        s = Session.objects.get(pk=request.session.session_key)
    except:
        return HttpResponseRedirect('/')
    c = request.COOKIES.get('csrftoken','')
    status = request.GET.get('status')
    username = s.get_decoded()['myname']
    team = Team.objects.filter(username=username)[0]
    tkobj = Ticket()
    try:
        ticketdata = tkobj.getallticketbystatusanddept(status,team.department.id)
    except:
        ticketdata = []
    tpl = tpl_lookup.get_template("undeobs_ticket.html")
    statusobj = TicketStatus()    
    status = statusobj.getallticketstatus()  
    return HttpResponse(tpl.render(csrf_token=c,on_home=True,ticket=ticketdata,status=status,userName=s.get_decoded()['myname']))

@csrf_exempt
def get_all_ticket_by_customername(request):
    try:
        s = Session.objects.get(pk=request.session.session_key)
    except:
        return HttpResponseRedirect('/')
    customerid =request.GET.get('customerid')
    c = request.COOKIES.get('csrftoken','')
    statusobj = TicketStatus()
    status = statusobj.getallticketstatus()
    ticketobj = Ticket()
    ticket = ticketobj.getallticketbycust(customerid)
    ticket.reverse()
    tpl = tpl_lookup.get_template("ticket_assign.html")    
    custobj = Customer()    
    customer = custobj.getallcustomer()
    department = Department.objects.all()
    statusobj = TicketStatus()    
    status = statusobj.getallticketstatus()
    teamobj = Team()
    teamdata = teamobj.getteamusertype("employee")
    return HttpResponse(tpl.render(csrf_token=c,on_home=True,status=status,datastatus=status,customer=customer,team=teamdata,department=department,userName=s.get_decoded()['myname'],ticket=ticket[0:20],first=0,last=20,count=len(ticket)))

    

@csrf_exempt
def get_all_ticket_by_companyname(request):
    try:
        s = Session.objects.get(pk=request.session.session_key)
    except:
        return HttpResponseRedirect('/')
    companyname =request.GET.get('companyname')
    c = request.COOKIES.get('csrftoken','')
    statusobj = TicketStatus()
    status = statusobj.getallticketstatus()
    ticketobj = Ticket()
    ticket = ticketobj.getallticketbycompany(companyname)
    ticket.reverse()
    tpl = tpl_lookup.get_template("ticket_assign.html")
    custobj = Customer()    
    customer = custobj.getallcustomer()
    department = Department.objects.all()
    statusobj = TicketStatus()    
    status = statusobj.getallticketstatus()
    teamobj = Team()
    teamdata = teamobj.getteamusertype("employee")
    return HttpResponse(tpl.render(csrf_token=c,on_home=True,status=status,datastatus=status,customer=customer,team=teamdata,department=department,userName=s.get_decoded()['myname'],ticket=ticket[0:20],first=0,last=20,count=len(ticket)))


@csrf_exempt
def get_all_ticket_by_departmentname(request):
    try:
        s = Session.objects.get(pk=request.session.session_key)
    except:
        return HttpResponseRedirect('/')
    departmentid =request.GET.get('departmentid')
    
    c = request.COOKIES.get('csrftoken','')
    statusobj = TicketStatus()
    status = statusobj.getallticketstatus()
    ticketobj = Ticket()
    ticket = ticketobj.getallticketbydept(departmentid)
    ticket.reverse()
    tpl = tpl_lookup.get_template("ticket_assign.html")
    custobj = Customer()    
    customer = custobj.getallcustomer()
    department = Department.objects.all()
    statusobj = TicketStatus()    
    status = statusobj.getallticketstatus()
    teamobj = Team()
    teamdata = teamobj.getteamusertype("employee")
    return HttpResponse(tpl.render(csrf_token=c,on_home=True,status=status,datastatus=status,customer=customer,team=teamdata,department=department,userName=s.get_decoded()['myname'],ticket=ticket[0:20],first=0,last=20,count=len(ticket)))


@csrf_exempt
def get_all_ticket_by_assignedname(request):
    try:
        s = Session.objects.get(pk=request.session.session_key)
    except:
        return HttpResponseRedirect('/')
    assignedid =request.GET.get('assignedid')
    c = request.COOKIES.get('csrftoken','')
    statusobj = TicketStatus()
    status = statusobj.getallticketstatus()
    ticketobj = Ticket()
    ticket = ticketobj.getticketbyassigneduser(assignedid)
    ticket.reverse()
    tpl = tpl_lookup.get_template("ticket_assign.html")
    custobj = Customer()    
    customer = custobj.getallcustomer()
    department = Department.objects.all()
    statusobj = TicketStatus()    
    status = statusobj.getallticketstatus()
    teamobj = Team()
    teamdata = teamobj.getteamusertype("employee")
    return HttpResponse(tpl.render(csrf_token=c,on_home=True,status=status,datastatus=status,customer=customer,team=teamdata,department=department,userName=s.get_decoded()['myname'],ticket=ticket[0:20],first=0,last=20,count=len(ticket)))


@csrf_exempt
def get_all_ticket_by_statusname(request):
    try:
        s = Session.objects.get(pk=request.session.session_key)
    except:
        return HttpResponseRedirect('/')
    ticketstatus =request.GET.get('status')
    c = request.COOKIES.get('csrftoken','')
    statusobj = TicketStatus()
    status = statusobj.getallticketstatus()
    ticketobj = Ticket()
    ticket = ticketobj.getticketbystatus(ticketstatus)
    ticket.reverse()
    tpl = tpl_lookup.get_template("ticket_assign.html")
    custobj = Customer()    
    customer = custobj.getallcustomer()
    department = Department.objects.all()
    statusobj = TicketStatus()    
    status = statusobj.getallticketstatus()
    teamobj = Team()
    teamdata = teamobj.getteamusertype("employee")
    return HttpResponse(tpl.render(csrf_token=c,on_home=True,status=status,datastatus=status,customer=customer,team=teamdata,department=department,userName=s.get_decoded()['myname'],ticket=ticket[0:20],first=0,last=20,count=len(ticket)))


@csrf_exempt
def departmentadmincreateticket(request):
    s = None
    try:
        s = Session.objects.get(pk=request.session.session_key)
    except:
        return HttpResponseRedirect('/')
    c = request.COOKIES.get('csrftoken','')
#        custobj = Customer.getAllCustomer()
    tpl = tpl_lookup.get_template("dept_create_ticket.html")
    statusList = TicketStatus.getallticketstatus()
    deptobj =Department()
    makeobj = Make()
    data = {"customerdata":custobj,"status":statusList,"statusList":statusList,"issue":deptobj.getalldept(),"make":makeobj.getallmake(),"userName":urllib.unquote(cookieuserName),"usertype":urllib.unquote(cookieuserType),"tkStatus":TicketStatus.getAllTicketStatus()}
    self.write(tpl.render(**data))

def customeradd(request):
    try:
        s = Session.objects.get(pk=request.session.session_key)
    except:
        return HttpResponseRedirect('/')
    c = request.COOKIES.get('csrftoken','')
    tpl = tpl_lookup.get_template("createcustomer.html")
    user = Alfreduser.objects.all()
    custpackage = CustomerPackage()
    statusobj = TicketStatus()    
    status = statusobj.getallticketstatus()
    return HttpResponse(tpl.render(csrf_token=c,on_home=True,allCustPackage=custpackage.getallcustomerpackage(),status=status,User=user,userName=s.get_decoded()['myname']))


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
        custpackage = request.POST.get('custpackage')
    except:
        custpackage = None
    custobj = Customer()
    if custobj.crcreatecustomer(username,password,email,customer_name,company_name,location,mobile,landline,custpackage):
        return HttpResponse(str(1))
    else:
        return HttpResponse(str(0))

@csrf_exempt
def customeredit(request):
    try:
        s = Session.objects.get(pk=request.session.session_key)
    except:
        return HttpResponseRedirect('/')
    c = request.COOKIES.get('csrftoken','')
    custId = request.GET.get('custId')
    custobj = Customer.getcustomerid(custId)
    customer = custobj
    c = request.COOKIES.get('csrftoken','')
    tpl = tpl_lookup.get_template("editcustomer.html")
    statusobj = TicketStatus()    
    status = statusobj.getallticketstatus()
    custpackage = CustomerPackage()
    return HttpResponse(tpl.render(csrf_token=c,on_home=True,customer=customer,status=status,allCustPackage=custpackage.getallcustomerpackage(),userName=s.get_decoded()['myname'])) 

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
    try:
        custpackage = request.POST.get('custpackage')
    except:
        custpackage = None
    custobj = Customer()
    if Customer.modifycustomer(custId,customer_name,company_name,email,location,mobile,landline,password,custpackage):
        return HttpResponse(str(1))
    else:
        return HttpResponse(str(0))

@csrf_exempt
def deletecustomer(request):
    try:
        s = Session.objects.get(pk=request.session.session_key)
    except:
        return HttpResponseRedirect('/')
    c = request.COOKIES.get('csrftoken','')
    custId = request.POST.get('custId')
    custobj = Customer()
    try:
        custobj.deletecustomer()
        return HttpResponse(str(1))
    except:
          return HttpResponse(str(0))

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
    statusobj = TicketStatus()    
    status = statusobj.getallticketstatus()
    deptobj = Department()
    dept = deptobj.getalldept()
    make = Make.objects.all()
    #data = {"customer":customerobj,"statusList":statusList,"issue":Issue.getAllIssueType(),"make":Make.getAllmakeType(),"userName":urllib.unquote(cookieuserName)}
    return HttpResponse(tpl.render(csrf_token=c,on_home=True,customer=customerobj[0],status=status,department=dept,make=make,userName=s.get_decoded()['myname']))

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
    custobj = Customer()
    customerobj = custobj.getcustomerid(custId)
    deptobj = Department()    
    deptobj = deptobj.getdepartmentbyid() 
    if custobj.createTicket(date,ticketid,custId,dept,system_id,problem,attachment):
        return HttpResponse(str(1))
    else:
        return HttpResponse(str(0))

@csrf_exempt
def createteamTicketform(request):
    s = None
    try:
        s = Session.objects.get(pk=request.session.session_key)
    except:
        return HttpResponseRedirect('/')
    c = request.COOKIES.get('csrftoken','')
    statusobj = TicketStatus()    
    status = statusobj.getallticketstatus()
    deptobj = Department()
    custobj = Customer()
    dept = deptobj.getalldept()
    make = Make.objects.all()    
    custdata = custobj.getallcustomer()
    tpl = tpl_lookup.get_template("dept_create_ticket.html")
    #data = {"customerdata":custobj,"status":TicketStatus.getAllTicketStatus(),"statusList":statusList,"issue":Issue.getAllIssueType(),"make":Make.getAllmakeType(),"userName":urllib.unquote(cookieuserName),"usertype":urllib.unquote(cookieuserType),"tkStatus":TicketStatus.getAllTicketStatus()}
    return HttpResponse(tpl.render(csrf_token=c,on_home=True,customerdata=custdata,status=status,department=dept,make=make,userName=s.get_decoded()['myname']))

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
    custobj = Customer()
    customerobj = custobj.getcustomerid(custId)
    deptobj = Department()    
    deptobj = deptobj.getdepartmentbyid() 
    if custobj.createTicket(date,ticketid,custId,dept,system_id,problem,attachment):
        return HttpResponse(str(1))
    else:
        return HttpResponse(str(0))

def createticketform(request):
    try:
        s = Session.objects.get(pk=request.session.session_key)
    except:
        return HttpResponseRedirect('/')
    c = request.COOKIES.get('csrftoken','')
    tpl = tpl_lookup.get_template("sadmin_create_ticket.html")
    custobj = Customer()    
    customer = custobj.getallcustomer()
    deptobj = Department()
    dept = deptobj.getalldept()
    user = Alfreduser.objects.all()
    statusobj = TicketStatus()    
    status = statusobj.getallticketstatus()
    return HttpResponse(tpl.render(csrf_token=c,on_home=True,department=dept,customer=customer,status=status,User=user,userName=s.get_decoded()['myname']))

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
    custobj = Customer()
    ticketobj = Ticket()
    customerobj = custobj.getcustomerid(custId)
    deptobj = Department()    
    deptobj = deptobj.getdepartmentbyid(dept) 
    if ticketobj.createTicket(date,ticketid,custId,dept,system_id,problem,attachment):
        return HttpResponse(str(1))
    else:
        return HttpResponse(str(0))
    
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
    

def ticketreports(request):
    try:
        s = Session.objects.get(pk=request.session.session_key)
    except:
        return HttpResponseRedirect('/')
    c = request.COOKIES.get('csrftoken','')
    tpl = tpl_lookup.get_template("report.html")
    user = Alfreduser.objects.all()
    statusobj = TicketStatus()    
    status = statusobj.getallticketstatus()
    return HttpResponse(tpl.render(csrf_token=c,on_home=True,status=status,User=user,userName=s.get_decoded()['myname'],date=strftime("%Y/%m/%d")))

def ticketreportscustomer(request):
    try:
        s = Session.objects.get(pk=request.session.session_key)
    except:
        return HttpResponseRedirect('/')
    c = request.COOKIES.get('csrftoken','')
    tpl = tpl_lookup.get_template("customerreport.html")
    user = Alfreduser.objects.all()
    statusobj = TicketStatus()    
    status = statusobj.getallticketstatus()
    return HttpResponse(tpl.render(csrf_token=c,on_home=True,status=status,User=user,userName=s.get_decoded()['myname'],date=strftime("%Y/%m/%d")))

def ticketreportsfeedback(request):
    try:
        s = Session.objects.get(pk=request.session.session_key)
    except:
        return HttpResponseRedirect('/')
    
def ticketassign(request):
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
    custobj = Customer()    
    customer = custobj.getallcustomer()
    department = Department.objects.all()
    statusobj = TicketStatus()    
    status = statusobj.getallticketstatus()
    teamobj = Team()
    teamdata = teamobj.getteamusertype("employee")
    return HttpResponse(tpl.render(csrf_token=c,on_home=True,datastatus=status,status=status,team=teamdata,customer=customer,department=department,userName=s.get_decoded()['myname'],ticket=ticket[0:20],first=0,last=20,count=len(ticket)))

@csrf_exempt
def departmentadmindashboard(request):
    s = None
    try:
        s = Session.objects.get(pk=request.session.session_key)
    except:
        return HttpResponseRedirect('/')
    c = request.COOKIES.get('csrftoken','')
    department = s.get_decoded()['department']
    username = s.get_decoded()['myname']
    tpl = tpl_lookup.get_template("admin_ticket_assign.html")
    ticketData = []
    tkobj = Ticket()
    ticketData = tkobj.getallticketbydept(department)
    ticketData.reverse()
    statusobj = TicketStatus()
    custobj = Customer()    
    customer = custobj.getallcustomer()
    teamobj = Team()
    assign = teamobj.getallteam()
    teamdata = teamobj.getteamusertype("employee")
    status = statusobj.getallticketstatus()
    return HttpResponse(tpl.render(csrf_token=c,on_home=True,ticket=ticketData,team=teamdata,customer=customer,status=status,datastatus=status,assign=assign,userName=s.get_decoded()['myname']))

@csrf_exempt
def sadminticketstatus(request):
    try:
        s = Session.objects.get(pk=request.session.session_key)
    except:
        return HttpResponseRedirect('/')
    c = request.COOKIES.get('csrftoken','')
    statusticket = request.GET.get('status')
    ticket = []
    ticketobjects = Ticket.objects.all()
    for i in ticketobjects:
       try:
           if i.status.id == status:
               ticket.append(i)
       except:
           pass
    tpl = tpl_lookup.get_template("open_ticket.html")
    statusobj = TicketStatus()
    status = statusobj.getallticketstatus()
    #data = {"userName":urllib.unquote(cookieuserName),"status":TicketStatus.getAllTicketStatus(),"ticket":tklist[0:20],"first":0,"last":20,"count":count}
    return HttpResponse(tpl.render(csrf_token=c,on_home=True,datastatus=status,statusticket=statusticket,status=status,userName=s.get_decoded()['myname'],ticket=ticket))

@csrf_exempt
def ticketdisplayinfo(request):
    try:
        s = Session.objects.get(pk=request.session.session_key)
    except:
        return HttpResponseRedirect('/')
    c = request.COOKIES.get('csrftoken','')
    statusobj = TicketStatus()
    status = statusobj.getallticketstatus()
    ticketId = request.GET.get('tkId')
    dept = Department()
    teamobj = Team()
    slaobj= Sla()
    makeobj = Make()
    tkobj = Ticket()
    ticketobject = tkobj.getTicketByTicketId(ticketId)
    allAssign=teamobj.getallteambydept(ticketobject.dept.id)
    tpl = tpl_lookup.get_template("ticket_assign_edit.html")
    return HttpResponse(tpl.render(csrf_token=c,on_home=True,ticket=ticketobject,status=status,allDept=dept.getalldept(),allMake=makeobj.getallmake(),allAssign=allAssign,allsla=slaobj.getallsla(),userName=s.get_decoded()['myname']))

@csrf_exempt
def departmentticketdisplay(request):
    try:
        s = Session.objects.get(pk=request.session.session_key)
    except:
        return HttpResponseRedirect('/')
    c = request.COOKIES.get('csrftoken','')
    department = s.get_decoded()['department']
    username = s.get_decoded()['myname']
    statusobj = TicketStatus()
    status = statusobj.getallticketstatus()
    print "status==",status
    ticketId = request.GET.get('tkId')
    print "ticketId==",ticketId
    dept = Department()
    print "dept==",dept
    teamobj = Team()
    print "teamobj==",teamobj
    slaobj= Sla()
    print "slaobj==",slaobj
    makeobj = Make()
    print "makeobj==",makeobj
    tkobj = Ticket()
    print "tkobj==",tkobj
    ticketobject = tkobj.getTicketByTicketId(ticketId)
    print "ticketobject==",ticketobject
    allAssign=teamobj.getallteambydept(ticketobject.dept.id)
    print "allAssign==",allAssign
    tpl = tpl_lookup.get_template("admin_ticket_assign_edit.html")
    return HttpResponse(tpl.render(csrf_token=c,on_home=True,ticket=ticketobject,status=status,allDept=dept.getalldept(),allMake=makeobj.getallmake(),allAssign=allAssign,allsla=slaobj.getallsla(),userName=s.get_decoded()['myname']))

def deleteticket(request):
    try:
        s = Session.objects.get(pk=request.session.session_key)
    except:
        return HttpResponseRedirect('/')
    c = request.COOKIES.get('csrftoken','')
    statusobj = TicketStatus()
    status = statusobj.getallticketstatus()
    ticketId = request.GET.get('tkId')
    ticketobj = Ticket()
    return HttpResponseRedirect('/ticket/assign')

@csrf_exempt
def assignticketdept(request):
    return HttpResponse(str(1))
    try:
        s = Session.objects.get(pk=request.session.session_key)
    except:
        return HttpResponseRedirect('/')
    c = request.COOKIES.get('csrftoken','')
    statusobj = TicketStatus()
    status = statusobj.getallticketstatus()
    ticketId = request.POST.get('ticketId')
    dept = request.POST.get('issueType')
    ticketobj = Ticket()
    if ticketobj.assignticket(ticketId,dept):
        return HttpResponse(str(1))
    else:
        return HttpResponse(str(0))

@csrf_exempt  
def assignticketdepartment(request):
    try:
        s = Session.objects.get(pk=request.session.session_key)
    except:
        return HttpResponseRedirect('/')
    c = request.COOKIES.get('csrftoken','')
    statusobj = TicketStatus()
    status = statusobj.getallticketstatus()
    ticketId = request.POST.get('ticketId')
    dept = request.POST.get('issueType')
    ticketobj = Ticket()
    if ticketobj.assignticketdept(ticketId,dept):
         return HttpResponse(str(1))
    else:
        return HttpResponse(str(0))
    
@csrf_exempt
def assignticketmember(request):
    try:
        s = Session.objects.get(pk=request.session.session_key)
    except:
        return HttpResponseRedirect('/')
    c = request.COOKIES.get('csrftoken','')
    statusobj = TicketStatus()
    status = statusobj.getallticketstatus()
    ticketId = request.POST.get('id')
    member = request.POST.get('asssigneTo')
    ticketobj = Ticket()
    if ticketobj.assignticketemployee(ticketId,member):
         return HttpResponse(str(1))
    else:
        return HttpResponse(str(0))


@csrf_exempt
def assignticketsla(request):
    try:
        s = Session.objects.get(pk=request.session.session_key)
    except:
        return HttpResponseRedirect('/')
    c = request.COOKIES.get('csrftoken','')
    statusobj = TicketStatus()
    status = statusobj.getallticketstatus()
    ticketId = request.POST.get('ticketId')
    sla = request.POST.get('sla')
    ticketobj = Ticket()
    if ticketobj.assignticketsla(ticketId,sla):
         return HttpResponse(str(1))
    else:
        return HttpResponse(str(0))

@csrf_exempt    
def getdetailsbyticketid(request):
    try:
        s = Session.objects.get(pk=request.session.session_key)
    except:
        return HttpResponseRedirect('/')
    c = request.COOKIES.get('csrftoken','')
    statusobj = TicketStatus()
    status = statusobj.getallticketstatus()
    id = request.GET.get('id')
    obj = Ticket()
    ticketobj = obj.getTicketByTicketId(id)
    tpl = tpl_lookup.get_template("teamdetails.html")
    return HttpResponse(tpl.render(csrf_token=c,on_home=True,ticket=ticketobj,status=status,userName=s.get_decoded()['myname']))

@csrf_exempt
def ticketstatusassign(request):
    try:
        s = Session.objects.get(pk=request.session.session_key)
    except:
        return HttpResponseRedirect('/')
    c = request.COOKIES.get('csrftoken','')
    statusobj = TicketStatus()
    status = statusobj.getallticketstatus()
    id = request.POST.get('id')
    status = request.POST.get('status')
    obj = Ticket()
    if obj.assignticketstatus(id,status):
        return HttpResponse(str(1))
    else:
        return HttpResponse(str(0))


def admin_get_all_ticket_report(request):
     try:
        s = Session.objects.get(pk=request.session.session_key)
     except:
        return HttpResponseRedirect('/')
     c = request.COOKIES.get('csrftoken','')
     tpl = tpl_lookup.get_template("report.html")
     statusobj = TicketStatus()
     deptobj = Department()
     dept = deptobj.getalldept()
     status = statusobj.getallticketstatus()
     return HttpResponse(tpl.render(on_home=True,status=status,userName=s.get_decoded()['myname'],department=dept,date=datetime.datetime.now().date()))
 
def admin_by_customer_report(request):
    try:
        s = Session.objects.get(pk=request.session.session_key)
    except:
        return HttpResponseRedirect('/')
    statusobj = TicketStatus()
    status = statusobj.getallticketstatus()
    tpl = tpl_lookup.get_template("customerreport.html")
    return HttpResponse(tpl.render(on_home=True,status=status,userName=s.get_decoded()['myname'],date=datetime.datetime.now().date()))

def admin_feedback_report(request):
    try:
        s = Session.objects.get(pk=request.session.session_key)
    except:
        return HttpResponseRedirect('/')
    statusobj = TicketStatus()
    status = statusobj.getallticketstatus()
    deptobj = Department()
    dept = deptobj.getalldept()
    tpl = tpl_lookup.get_template("feedbackreport.html")
    return HttpResponse(tpl.render(on_home=True,status=status,department=dept,userName=s.get_decoded()['myname'],date=datetime.datetime.now().date()))
