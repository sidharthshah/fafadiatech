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
        request.session['department'] = urllib.quote(str(userobj.deparment))
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

def teamdashboard(request):
    c = request.COOKIES.get('csrftoken','')
    tpl = tpl_lookup.get_template("teamsummary.html")
    team = Team.objects.all()
    status = TicketStatus.objects.all()
    return HttpResponse(tpl.render(csrf_token=c,on_home=True,status=status,team=team,userName='Smita'))

def addteamform(request):
    c = request.COOKIES.get('csrftoken','')
    tpl = tpl_lookup.get_template("createteam.html")
    dept = Deparment.objects.all()
    user = []#Alfreduser.objects.all()
    status = TicketStatus.objects.all()
    return HttpResponse(tpl.render(csrf_token=c,on_home=True,dept=dept,status=status,User=user,userName='Smita'))

@csrf_exempt
def teamadd(request):
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
    deptobj = Deparment.objects.filter(id=dept)[0]
    try:
        teamobj = Team(username=name,password=password,name=name,address=address,landlineno=landline,mobileno=mobile,email=email,deparment=deptobj,usertype=usertype)
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
        print  obj
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
    try:      
        deptobj = CustomerPackage(package_type=customerpackage)
        deptobj.save() 
        return HttpResponse(str(1))   
    except:
        return HttpResponse(str(0))
    
def customerpackageedit(request):
    c = request.COOKIES.get('csrftoken','')
    packageid = request.POST.get('packageid')
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
    try:
        custpkgobj = CustomerPackage.objects.filter(id=packageid).update(package_type=packagetype)
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
    try:      
        slaobj = Sla(slatype=sla)
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
    try:
        custpkgobj = Sla.objects.filter(id=slaid).update(slatype=slatype)
        return HttpResponse(str(1))
    except:
        custpkgobj = None
        return HttpResponse(str(0))

@csrf_exempt
def sladelete(request):
    c = request.COOKIES.get('csrftoken','')
    slaid = request.POST.get('slaid')
    try:
        obj = CustomerPackage.objects.filter(id=slaid).delete()
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
    try:      
        ticketstatusobj = TicketStatus(statustype=statustype)
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
    try:
        custpkgobj = TicketStatus.objects.filter(id=statusId).update(statustype=statustype)
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
    obj = Deparment.objects.filter(id=deptid).update(department=dept)
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
    c = request.COOKIES.get('csrftoken','')
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
    try:
        password = 'smita'
    except:
        password =None
    obj = Customer.objects.filter(id=custId).update(name=customer_name,company=company_name,email=email,address=location,mobile=mobile,landline=landline,password=password)
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

def createticketform(request):
    c = request.COOKIES.get('csrftoken','')
    tpl = tpl_lookup.get_template("sadmin_create_ticket.html")
    customer = Customer.objects.all()
    deparment = Deparment.objects.all()
    user = Alfreduser.objects.all()
    status = TicketStatus.objects.all()
    return HttpResponse(tpl.render(csrf_token=c,on_home=True,deparment=deparment,customer=customer,status=status,User=user,userName='Smita'))

@csrf_exempt
def createticket(request):
    date = datetime.datetime.now()
    try:
        custId = request.POST.get('customer')
    except:
        custId = None
    print "custId==",custId
    try:
        system_id =request.POST.get('system_id')
    except:
        system_id = None
    print "system_id==",system_id
    try:
        problem = request.POST.get('problem')
    except:
        problem = None
    print "problem==",problem
    try:
        dept=request.POST.get("issue_type")
    except:
        dept = None
    print dept
    try:
        attachment = request.POST.get("files")
    except:
        attachment = None
    ticketid ="PSSPL/"+strftime("%y/%m/%d/%H/%M/%S")
    
    customerobj = Customer.objects.filter(id=custId)[0]
    print "customerobj",customerobj
    deptobj = Deparment.objects.filter(id=dept)[0]
    print "deptobj",deptobj
    
    ticketobj = Ticket.objects.create(ts=date,ticketid=ticketid,customer=customerobj,dept=deptobj,systemid=system_id,summary=problem,attachment=attachment)

    #customer=custId,dept=dept,systemid=systemid,
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
