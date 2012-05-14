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
    alluser = Alfreduser.objects.all()
    for i in alluser:
        if i.username == uname and i.password==passwd:
            return i
    return None

def home(request):
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
    if userobj: 
        request.session.set_expiry(300)
        request.session['userid']=urllib.quote(str(userobj.id))
        request.session['last_login'] = datetime.datetime.now()
        request.session['myname'] = urllib.quote(userobj.username)
        request.session['department'] = urllib.quote(str(userobj.department))
        request.session['type'] = urllib.quote(userobj.usertype)
        request.session.modified = True
        return HttpResponse(str(1))
    else:
        return HttpResponse(str(0))

def userdashboard(request):
    try:
        s = Session.objects.get(pk=request.session.session_key)
        c = request.COOKIES.get('csrftoken','')
        tpl = tpl_lookup.get_template("usrsummry.html")
        user = Alfreduser.objects.all()
        status = TicketStatus.objects.all()
        return HttpResponse(tpl.render(csrf_token=c,on_home=True,status=status,User=user,userName=s.get_decoded()['myname']))
    except:
        return HttpResponseRedirect('/')

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

def dashboard(request):
    c = request.COOKIES.get('csrftoken','')
    tpl = tpl_lookup.get_template("dashboard.html")
    team = Team.objects.all()
    status = TicketStatus.objects.all()
    return HttpResponse(tpl.render(csrf_token=c,on_home=True,status=status,team=team,userName='Smita'))

def addteamform(request):
    c = request.COOKIES.get('csrftoken','')
    tpl = tpl_lookup.get_template("createteam.html")
    user = []#Alfreduser.objects.all()
    status = TicketStatus.objects.all()
    return HttpResponse(tpl.render(csrf_token=c,on_home=True,status=status,User=user,userName='Smita'))

@csrf_exempt
def teamadd(request):
    name = request.POST.get('name')
    password=request.POST.get('password')
    address = request.POST.get('address')
    landline = request.POST.get('landline')
    mobile = request.POST.get('mobile')
    email = request.POST.get('email')
    try:
        teamobj = Team(username=name,password=password,name=name,address=address,landlineno=landline,mobileno=mobile,email=email)
        teamobj.save()
        return HttpResponse(str(1))   
    except:
        return HttpResponse(str(0))    
        
@csrf_exempt
def teameditform(request):
    c = request.COOKIES.get('csrftoken','')
    tpl = tpl_lookup.get_template("editteam.html")
    teamid = request.POST.get('teamId')
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
    department = Department.objects.all() 
    return HttpResponse(tpl.render(csrf_token=c,on_home=True,status=status,department=department,userName='Smita'))


@csrf_exempt
def departmentadd(request):
    c = request.COOKIES.get('csrftoken','')
    department = request.POST.get('department')
    newdepartment=department.title()
    try:      
        deptobj = Department(department=newdepartment)
        deptobj.save()
        return HttpResponse(str(1))   
    except:
        return HttpResponse(str(0))
    
def departmentedit(request):
    c = request.COOKIES.get('csrftoken','')
    deptid = request.GET.get('deptid')
    try:
        deptobj = Department.objects.filter(id=deptid)
    except:
        deptobj = None
    tpl = tpl_lookup.get_template("editissuemaster.html")
    status = TicketStatus.objects.all()
    return HttpResponse(tpl.render(csrf_token=c,on_home=True,status=status,dept=deptobj[0],userName='Smita'))

@csrf_exempt
def departmentmodify(request):
    c = request.COOKIES.get('csrftoken','')
    deptid = request.POST.get('deptid')
    dept = request.POST.get('dept')
    newdept = dept.title()
    obj = Department.objects.filter(id=deptid).update(department=newdept)
    return HttpResponse(str(obj))

@csrf_exempt
def deletedepartment(request):
    c = request.COOKIES.get('csrftoken','')
    deptid = request.POST.get('deptid')  
    try:
        obj = Department.objects.filter(id=deptid).delete()
        return HttpResponse(str(1))
    except:
        return HttpResponse(str(0))
   
def customerpackagedashboard(request):
    c = request.COOKIES.get('csrftoken','')
    tpl = tpl_lookup.get_template("customerpackage.html")
    status = TicketStatus.objects.all()
    customerpackage = CustomerPackage.objects.all() 
    return HttpResponse(tpl.render(csrf_token=c,on_home=True,status=status,customerpackage=customerpackage,userName='Smita'))

@csrf_exempt
def customerpackageadd(request):
    c = request.COOKIES.get('csrftoken','')
    customerpackage = request.POST.get('customer_package')
    newcustomerpackage=customerpackage.title()
    try:      
        deptobj = CustomerPackage(package_type=newcustomerpackage)
        deptobj.save() 
        return HttpResponse(str(1))   
    except:
        return HttpResponse(str(0))
    
def customerpackageedit(request):
    c = request.COOKIES.get('csrftoken','')
    packageid = request.GET.get('packageid')
    try:
        custpkgobj = CustomerPackage.objects.filter(id=packageid)
    except:
        custpkgobj = None
    tpl = tpl_lookup.get_template("editcustomerpackage.html")
    status = TicketStatus.objects.all()
    return HttpResponse(tpl.render(csrf_token=c,on_home=True,status=status,custpkg=custpkgobj[0],userName='Smita'))

@csrf_exempt
def customerpackagemodify(request):
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
    c = request.COOKIES.get('csrftoken','')
    customerpackageid = request.POST.get('customerpackageid')
    try:
        obj = CustomerPackage.objects.filter(id=customerpackageid).delete()
        return HttpResponse(str(1))
    except:
        return HttpResponse(str(0))

def sladashboard(request):
    c = request.COOKIES.get('csrftoken','')
    tpl = tpl_lookup.get_template("slatype.html")
    status = TicketStatus.objects.all()
    sla = Sla.objects.all() 
    return HttpResponse(tpl.render(csrf_token=c,on_home=True,status=status,sla=sla,userName='Smita'))

@csrf_exempt
def slaadd(request):
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
    c = request.COOKIES.get('csrftoken','')
    slaid = request.GET.get('slaid')
    print slaid
    try:
        slaobj = Sla.objects.filter(id=slaid)
    except:
        slaobj = None
    tpl = tpl_lookup.get_template("editslatype.html")
    status = TicketStatus.objects.all()
    return HttpResponse(tpl.render(csrf_token=c,on_home=True,status=status,slaobj=slaobj[0],userName='Smita'))

@csrf_exempt
def slamodify(request):
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
    c = request.COOKIES.get('csrftoken','')
    slaid = request.POST.get('slaid')
    try:
        obj = Sla.objects.filter(id=slaid).delete()
        return HttpResponse(str(1))
    except:
        return HttpResponse(str(0))

def ticketstatusdashboard(request):
    c = request.COOKIES.get('csrftoken','')
    tpl = tpl_lookup.get_template("ticketstatusmaster.html")
    status = TicketStatus.objects.all()
    return HttpResponse(tpl.render(csrf_token=c,on_home=True,ticket=status,status=status,userName='Smita'))

@csrf_exempt
def ticketstatusadd(request):
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
    c = request.COOKIES.get('csrftoken','')
    statusId = request.GET.get('statusId')
    try:
        statusobj = TicketStatus.objects.filter(id=statusId)
    except:
        statusobj = None
    tpl = tpl_lookup.get_template("editticketstatus.html")
    status = TicketStatus.objects.all()
    return HttpResponse(tpl.render(csrf_token=c,on_home=True,status=status,statusobj=statusobj[0],userName='Smita'))

@csrf_exempt
def ticketstatusmodify(request):
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
    c = request.COOKIES.get('csrftoken','')
    statusId = request.POST.get('statusId')
    try:
        obj = TicketStatus.objects.filter(id=statusId).delete()
        return HttpResponse(str(1))
    except:
        return HttpResponse(str(0))

def customersummary(request):
    c = request.COOKIES.get('csrftoken','')
    tpl = tpl_lookup.get_template("customersummary.html")
    customer = Customer.objects.all()
    user = Alfreduser.objects.all()
    status = TicketStatus.objects.all()
    return HttpResponse(tpl.render(csrf_token=c,on_home=True,customer=customer,status=status,User=user,userName='Smita'))

@csrf_exempt
def modifydepartment(request):
    c = request.COOKIES.get('csrftoken','')
    deptid = request.POST.get('deptid')
    dept = request.POST.get('dept')
    obj = Department.objects.filter(id=deptid).update(department=dept)
    return HttpResponse(str(obj))

def customeradd(request):
    c = request.COOKIES.get('csrftoken','')
    tpl = tpl_lookup.get_template("createcustomer.html")
    user = Alfreduser.objects.all()
    status = TicketStatus.objects.all()
    return HttpResponse(tpl.render(csrf_token=c,on_home=True,status=status,User=user,userName='Smita'))

def editcustomer(request):
     c = request.COOKIES.get('csrftoken','')
     custid = request.GET.get('teamId')
     cust = CustomerPackage.objects.filter(id=slaid)

@csrf_exempt
def customeraddpost(request):
    name="dfdfdfdf"
    password = "aksakjs"
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
        custobj = Customer(username=name,password=password,name=customer_name,company=company_name,address=location,mobile=mobile,landline=landline)
        custobj.save()
        return HttpResponse(str(1))   
    except:
        return HttpResponse(str(0))  


def customeredit(request):
    custId = request.GET.get('custId')
    customer = Customer.objects.filter(id=custId)[0]
    c = request.COOKIES.get('csrftoken','')
    tpl = tpl_lookup.get_template("editcustomer.html")
    user = Alfreduser.objects.all()
    status = TicketStatus.objects.all()
    return HttpResponse(tpl.render(csrf_token=c,on_home=True,customer=customer,status=status,User=user,userName='Smita'))


    

@csrf_exempt
def customermodify(request):
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
    obj = Customer.objects.filter(id=custId).update(name=customer_name,company=company_name,email=email,address=location,mobile=mobile,landline=landline)
    return HttpResponse(str(obj))

@csrf_exempt
def deletecustomer(request):
    c = request.COOKIES.get('csrftoken','')
    custId = request.POST.get('custId')
    obj = Customer.objects.filter(id=custId).delete()
    return HttpResponse(str(1))

def customercreateticket():
    c = request.COOKIES.get('csrftoken','')
    tpl = tpl_lookup.get_template("ticket.html")
    user = Alfreduser.objects.all()
    status = TicketStatus.objects.all()
    return HttpResponse(tpl.render(csrf_token=c,on_home=True,status=status,User=user,userName='Smita'))

def createticket(request):
    c = request.COOKIES.get('csrftoken','')
    tpl = tpl_lookup.get_template("sadmin_create_ticket.html")
    customer = Customer.objects.all()
    department = Department.objects.all()
    user = Alfreduser.objects.all()
    status = TicketStatus.objects.all()
    return HttpResponse(tpl.render(csrf_token=c,on_home=True,department=department,customer=customer,status=status,User=user,userName='Smita'))

@csrf_exempt
def createticketpost(request):
    date = datetime.datetime.now()
    try:
        custId = request.POST.get('customer')
    except:
        custId = None
    print "custId==",custId
    try:
        customer = request.POST.get('customer')
    except:
        customer = None
    print "customer==",customer
    try:
        company_name = request.POST.get('company_name')
    except:
        company_name = None
    print "company_name==",company_name
    try:
        email = request.POST.get('email')
    except:
        email = None
    print "email==",email
    try:
        location = request.POST.get('location')
    except:
        location = None
    print "location==",location
    try:
        mobile = request.POST.get('mobile')
    except:
        mobile = None
    print "mobile==",mobile
    try:
        landline = request.POST.get('landline')
    except:
        landline = None
    print "landline==",landline
    try:
        system_id =self.get_argument('system_id')
    except:
        system_id = None
    print "system_id==",system_id
    try:
        problem = self.get_argument('problem')
    except:
        problem = None
    print "problem==",problem
    try:
        issue_type=self.get_argument("issue_type")
    except:
        issue_type = None
    print "issue_type==",issue_type
    ticketid ="PSSPL/"+strftime("%y/%m/%d/%H/%M/%S")
    ticketobj = Ticket(ts=date,ticketid=ticketid,customer=customer,dept=issue_type,systemid=system_id,summary=problem)
    ticketobj.save()
    c = request.COOKIES.get('csrftoken','')
    tpl = tpl_lookup.get_template("sadmin_create_ticket.html")
    user = Alfreduser.objects.all()
    status = TicketStatus.objects.all()
    return HttpResponse(tpl.render(csrf_token=c,on_home=True,status=status,User=user,userName='Smita'))

@csrf_exempt
def dispcustomerdata(request):
    c = request.COOKIES.get('csrftoken','')
    custId = request.POST.get('customerid')
    obj = Customer.objects.filter(id=custId)
    listdata = []
    for i in obj:
        listdata.append((i.name,i.company,i.address,i.landline,i.mobile,i.email))
    dict = {"data":listdata[0]}
    return HttpResponse(json.dumps(dict))
    return HttpResponse(tpl.render(csrf_token=c,on_home=True,customer=customer,status=status,User=user,userName='Smita'))

def ticketreports(request):
    c = request.COOKIES.get('csrftoken','')
    tpl = tpl_lookup.get_template("report.html")
    user = Alfreduser.objects.all()
    status = TicketStatus.objects.all()
    department = Department.objects.all()
    return HttpResponse(tpl.render(csrf_token=c,on_home=True,status=status,User=user,department=department,userName='Smita',date=strftime("%Y/%m/%d")))

def ticketreportscustomer(request):
    c = request.COOKIES.get('csrftoken','')
    tpl = tpl_lookup.get_template("customerreport.html")
    user = Alfreduser.objects.all()
    status = TicketStatus.objects.all()
    return HttpResponse(tpl.render(csrf_token=c,on_home=True,status=status,User=user,userName='Smita',date=strftime("%Y/%m/%d")))

def ticketreportsfeedback(request):
    c = request.COOKIES.get('csrftoken','')
    tpl = tpl_lookup.get_template("feedbackreport.html")
    user = Alfreduser.objects.all()
    status = TicketStatus.objects.all()
    department = Department.objects.all()
    return HttpResponse(tpl.render(csrf_token=c,on_home=True,status=status,User=user,department=department,userName='Smita',date=strftime("%Y/%m/%d")))
