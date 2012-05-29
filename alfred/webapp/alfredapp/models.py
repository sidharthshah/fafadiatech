import os
from django.db import models
from django.contrib.auth.models import User, UserManager

STATIC_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)),"..","static","attachments")

class Department(models.Model):
    department = models.CharField(max_length=30)

    def __unicode__(self):
        return self.department
    
    def getalldept(self):
        return Department.objects.all()

class SettingsBackend(object):
    """
    Authenticate against the settings ADMIN_LOGIN and ADMIN_PASSWORD.

    Use the login name, and a hash of the password. For example:

    ADMIN_LOGIN = 'admin'
    ADMIN_PASSWORD = 'sha1$4e987$afbcf42e21bd417fb71db8c66b321e9fc33051de'
    """

    def authenticate(self, username=None, password=None):
        login_valid = (settings.ADMIN_LOGIN == username)
        pwd_valid = check_password(password, settings.ADMIN_PASSWORD)
        if login_valid and pwd_valid:
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                # Create a new user. Note that we can set password
                # to anything, because it won't be checked; the password
                # from settings.py will.
                user = User(username=username, password='get from settings.py')
                user.is_staff = True
                user.is_superuser = True
                user.save()
            return user
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None



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



class Sla(models.Model):
    slatype = models.CharField(max_length=50)

    def __unicode__(self):
        return self.slatype
    
    def getallsla(self):
        return Sla.objects.all()

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
        return Ticket.objects.filter(id=ticketid)
    
    
    def getdatewiseticket(self,date):
        alldata = []
        for i in Ticket.objects.all():
            if i.ts.date() == date.date():
                alldata.append(i)
        return alldata
            
        
    def getallticketbycust(self,cust):
        ticket = []
        allTicket = Ticket.objects.all()
        for i in allTicket:
            if i.customer.id == cust.id:
                ticket.append(i)
        ticket.reverse()
        return ticket
    
    def getticketbystatusandcust(self,status,cust):
        datalist = []
        tkobj = Ticket.objects.all()
        for i in tkobj:
            try:
                if i.status.id == status and i.customer.id==cust :
                        datalist.append(i)
            except:
                pass
        return datalist
    
    def getticketbyassigneduser(self,user):
        allteamdata = []
        tkobj = Ticket.objects.all()
        for i in tkobj:
            try:
                if i.assignedto is user:
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
                if i.dept.id == department:
                    datalist.append(i)
            except:
                pass
        return datalist
    
    def deleteTicketyTicketId(self,ticketid):
        pass
    
    
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
    

class Note(models.Model):
    user = models.ForeignKey(User)
    pub_date = models.DateTimeField()
    title = models.CharField(max_length=200)
    body = models.TextField()

    def __unicode__(self):
        return self.title
