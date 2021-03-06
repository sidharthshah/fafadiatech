import os
from django.db import models
from django.contrib.auth.models import User, UserManager
from django.db.models import Q

STATIC_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)),"..","static","attachments")

class Department(models.Model):
    department = models.CharField(max_length=30)

    def __unicode__(self):
        return self.department
    
    def getalldept(self):
        return Department.objects.all()
    
    def getdepartmentbyid(self,dept):
        return Department.objects.filter(id=dept)[0]


class Alfreduser(User):
    USER_TYPE_CHOICES =  (('superadmin','superadmin'),('departmentadmin','departmentadmin'),('customer','customer'),('employee','employee'),)
    usertype = models.CharField(max_length=30,choices=USER_TYPE_CHOICES,default=None)
    department = models.ForeignKey(Department,default=None)
    objects = UserManager()

    def __unicode__(self):
        return self.usertype

class TicketStatus(models.Model):
    statustype = models.CharField(max_length=30)

    def __unicode__(self):
        return self.statustype
    
    def getallticketstatus(self):
        return TicketStatus.objects.all()

class Team(User):
    USER_TYPE_CHOICES =  (('superadmin','superadmin'),('departmentadmin','departmentadmin'),('customer','customer'),('employee','employee'),)
    usertype = models.CharField(max_length=30,choices=USER_TYPE_CHOICES,default=None)
    department = models.ForeignKey(Department,default=None,blank=True,null=True)
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=250)
    landlineno = models.CharField(max_length=15)
    mobileno =  models.CharField(max_length=11)
    #email = models.EmailField()

    def __unicode__(self):
        return self.name
    
    def getallteam(self):
        return Team.objects.all()
    
    def getteammemberbyid(self,teamid):
        return Team.objects.filter(id=teamid)
    
    def getallteambydept(self,dept):
        listdata = []
        try:
            deptobj = Department.objects.filter(id=dept)
            allteam = Team.objects.filter(department=deptobj)
            for i in allteam:
                if i.usertype == 'employee':
                    listdata.append(i)               
            return listdata
        except:
            return 0
        
    def getteamusertype(self,usertype):
        return Team.objects.filter(usertype=usertype)
        
        

class CustomerPackage(models.Model):
    package_type = models.CharField(max_length=50)
    

    def __unicode__(self):
        return self.package_type
    
    def getallcustomerpackage(self):
        return CustomerPackage.objects.all()
    
    def getcustomerpackagebyid(self,id):
        try:
            return CustomerPackage.objects.filter(id=id)[0]
        except:
            return None
        
class Customer(User):
    name = models.CharField(max_length=100)
    company = models.CharField(max_length=50)
    address = models.CharField(max_length=255)
    landline = models.CharField(max_length=15)
    mobile = models.CharField(max_length=11)
    alternatemobile = models.CharField(max_length=11)
    alternateemail = models.EmailField()
    package = models.ForeignKey(CustomerPackage,blank=True,null=True)

    def __unicode__(self):
        return self.name
    
    def getallcustomer(self):
        return Customer.objects.all()
    
    def getcustomerid(self,custid):
        return Customer.objects.filter(id=custid)[0]
    
    def createcustomer(self,username,password,email,customer_name,company_name,location,mobile,landline,custpackage):
        obj = CustomerPackage()
        custpkgobj = obj.getcustomerpackagebyid(custpackage)
        try:
            custobj = Customer(username=username,password=password,email=email,name=customer_name,company=company_name,address=location,mobile=mobile,landline=landline,package=custpkgobj)
            custobj.save()
            return 1
        except:
            return 0
    
    def modifycustomer(self,custId,customer_name,company_name,email,location,mobile,landline,password,custpackage):
        custpkgobj = CustomerPackage()
        custpakg = custpkgobj.getcustomerpackagebyid(custpackage)
        try:
            obj = Customer.objects.filter(id=custId).update(name=customer_name,company=company_name,email=email,address=location,mobile=mobile,landline=landline,password=password,package=custpakg)
            return 1
        except:
            return 0
        
    def deletecustomer(self,custId):
        try:
            Customer.objects.filter(id=custId).delete()
            return 1
        except:
            return 0

class Sla(models.Model):
    slatype = models.CharField(max_length=50)

    def __unicode__(self):
        return self.slatype
    
    def getallsla(self):
        return Sla.objects.all()
    
    def getslabyid(self,id):
        return Sla.objects.filter(id=id)
    
class Dsk(models.Model):
    dsktype = models.CharField(max_length=50)

    def __unicode__(self):
        return self.dsktype

class Make(models.Model):
    make = models.CharField(max_length=50)

    def __unicode__(self):
        return self.make
    
    def getallmake(self):
        return Make.objects.all()

class Ticket(models.Model):
    ts= models.DateTimeField()
    ticketid = models.CharField(max_length=30)
    customer = models.ForeignKey(Customer)
    dept = models.ForeignKey(Department,blank=True,null=True)
    systemid = models.CharField(max_length=255)
    summary = models.CharField(max_length=255)
    status = models.ForeignKey(TicketStatus,blank=True,null=True)
    assignedto = models.ForeignKey(Team,blank=True,null=True)
    sla = models.ForeignKey(Sla,blank=True,null=True)
    attachment = models.FileField(upload_to=STATIC_PATH,blank=True,null=True)
   # package = models.ForeignKey(CustomerPackage,blank=True,null=True)

    def __unicode__(self):
        return self.ticketid
    
    def getallticket(self):
        return Ticket.objects.all()
    
    def getTicketByTicketId(self,ticketid):
        return Ticket.objects.filter(id=ticketid)[0]

    def getdatewiseticket(self,date):
        alldata = []
        for i in Ticket.objects.all():
            if i.ts.date() == date.date():
                alldata.append(i)
        return alldata

    def getallticketbycust(self,cust):
        custobj = Customer.objects.filter(id=cust)[0]
        ticket = []
        allTicket = Ticket.objects.all()
        for i in allTicket:
            if i.customer.id == custobj.id:
                ticket.append(i)
        ticket.reverse()
        return ticket

    def getallticketbyticket(self,ticketid):
        print "gfgdfg"
        tkobj = Ticket.objects.filter(id=ticketid)
        print "tkobj==",tkobj
        ticket = []
        allTicket = Ticket.objects.all()
        print "allTicket",allTicket
        for i in allTicket:
            print "i.ticketid.id==",i.ticketid.id
            if i.ticketid.id == tkobj.id:
                ticket.append(i)
        ticket.reverse()
        return ticket

    def getallticketbycompany(self,company):
        allTicket = Ticket.objects.all()
        ticket = []
        for i in allTicket:
            if i.customer.company == company:
                ticket.append(i)
        ticket.reverse()
        return ticket

    def getticketbystatusandcust(self,status,cust):
        datalist = []
        tkobj = Ticket.objects.all()
        for i in tkobj:
            try:
                if i.status.id == status and i.customer.id==cust:
                        datalist.append(i)
            except:
                pass
        return datalist
    
    def getticketbystatus(self,status):
        datalist = []
        tkobj = Ticket.objects.all()
        for i in tkobj:
            if i.status:
                if i.status.id == int(status):
                    datalist.append(i)
        return datalist
        
    def getticketbyassigneduser(self,user):
        allteamdata = []
        teamobj = Team.objects.filter(id = user)[0]
        tkobj = Ticket.objects.all()
        for i in tkobj:
            try:
                if i.assignedto.id == teamobj.id:
                    allteamdata.append(i)
            except:
                pass
        return allteamdata
    
    def getticketbyassigneduserdept(self,user,dept):
        allteamdata = []
        teamobj = Team.objects.filter(id = user)[0]
        tkobj = Ticket.objects.all()
        for i in tkobj:
            try:
                if i.assignedto.id == teamobj.id and i.dept.id == dept:
                    allteamdata.append(i)
            except:
                pass
        return allteamdata

    def getallticketbystatusanddept(self,status,dept):
        datalist = []
        tkobj = Ticket.objects.all()
        for i in tkobj:
            try:
                if i.status.id == status and i.department.id==dept :
                        datalist.append(i)
            except:
                pass
        return datalist
    
    def getallticketbydept(self,department):
        datalist = []
        tkobj = Ticket.objects.all()
        for i in tkobj:
            try:
                if i.dept.id == int(department):
                    datalist.append(i)
            except:
                pass
        return datalist

    def getallticketbycustomername(self,customername):
        datalist = []
        tkobj = Ticket.objects.all()
        for i in tkobj:
            try:
                if i.customer.id == customername:
                    datalist.append(i)
            except:
                pass
        return datalist
    
    def getticketbycustassigneduser(self,cust,dept):
        datalist = []
        obj = Department()
        deptobj = obj.getdepartmentbyid(dept)
        tkobj = Ticket.objects.all()
        for i in tkobj:
            try:
                if i.customer.id == cust and i.dept.id == deptobj.id:
                    datalist.append(i)
            except:
                pass
        return datalist
    
    def getallticketbycompanydept(self,customername,dept):
        datalist = []
        obj = Department()
        deptobj = obj.getdepartmentbyid(dept)
        tkobj = Ticket.objects.all()
        for i in tkobj:
            try:
                if i.customer.id == customername and i.dept.id == deptobj.id:
                    datalist.append(i)
            except:
                pass
        return datalist
    
    
    def getallticketbycustdept(self,cust,dept):
        print cust,dept
        datalist = []
        tkobj = Ticket.objects.all()
        obj = Department()
        dept = obj.getdepartmentbyid(dept)
        for i in tkobj:
            try:
                if i.customer.id == int(cust) and i.dept.id == dept.id:
                    datalist.append(i)
            except:
                pass
        return datalist
    

    def assignticketdept(self,id,dept):
        obj = Department()
        deptobj = obj.getdepartmentbyid(dept)
        try:
            Ticket.objects.filter(id=id).update(dept=deptobj)
            return 1
        except:
            return 0
        
    def assignticketemployee(self,id,member):
        obj = Team()
        teamobj = obj.getteammemberbyid(member)[0]
        try:
            Ticket.objects.filter(id=id).update(assignedto=teamobj)
            return 1
        except:
            return 0

    def assignticketsla(self,id,sla):
        obj = Sla()
        slaobj = obj.getslabyid(sla)[0]
        try:
            Ticket.objects.filter(id=id).update(sla=slaobj)
            return 1
        except:
            return 0
    
    def createTicket(self,date,ticketid,custId,dept,system_id,problem,attachment):
        custobj = Customer()
        customerobj = custobj.getcustomerid(custId)
        
        deptobj = Department()    
        deptobj = deptobj.getdepartmentbyid(dept) 
        try:
            ticketobj = Ticket.objects.create(ts=date,ticketid=ticketid,customer=customerobj,dept=deptobj,systemid=system_id,summary=problem,attachment=attachment)
            ticketobj.save()
            return 1
        except:
            return 0
    
    def deleteticketbyticketid(self,ticketId):
        return Ticket.objects.filter(id=ticketId).delete()
    
    def assignticketstatus(self,id,status):
        statusobj = TicketStatus.objects.filter(id=status)[0]
        Ticket.objects.filter(id=id).update(status=statusobj)
        try:
            Ticket.objects.filter(id=id).update(status=statusobj)
            return 1
        except:
            return 0
    
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
    

class TicketActivity(models.Model):
    ts= models.DateTimeField()
    customer =  models.ForeignKey(Customer,blank=True,null=True)
    team =  models.ForeignKey(Team,blank=True,null=True)
    ticketactivity = models.CharField(max_length=200)
    
    def addcustomerticketactivity(self,ts,user,ticketactivity):
        custobj = Customer.objects.filter(id=user)
        tkactobj = TicketActivity()
        try:
            ticketactobj = tkactobj.objects.create(ts=date,customer=custobj,ticketactivity=ticketactivity)
            ticketactobj.save()
            return 1
        except:
            return 0
        
    def addteamaticketactivity(self,user,ticketactivity):
        teamobj = Team.objects.filter(id=user)
        tkactobj = TicketActivity()
        try:
            ticketactobj = tkactobj.objects.create(ts=date,team=teamobj,ticketactivity=ticketactivity)
            ticketactobj.save()
            return 1
        except:
            return 0
        
    def getticketactivity(self,id):
        return TicketActivity.objects.filter(id=id)
        
    
class Note(models.Model):
    user = models.ForeignKey(User)
    pub_date = models.DateTimeField()
    title = models.CharField(max_length=200)
    body = models.TextField()

    def __unicode__(self):
        return self.title
