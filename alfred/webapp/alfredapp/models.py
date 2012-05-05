import os
from django.db import models
from django.contrib.auth.models import User, UserManager

STATIC_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)),"..","static","attachments")

class Deparment(models.Model):
    department = models.CharField(max_length=30)

    def __unicode__(self):
        return self.department

class Alfreduser(User):
    USER_TYPE_CHOICES =  (('superadmin','superadmin'),('departmentadmin','departmentadmin'),('customer','customer'),('employee','employee'),)
    usertype = models.CharField(max_length=30,choices=USER_TYPE_CHOICES)
    def total_department(self):
        departmemt = []
        for eachdept in Deparment.objects.all():
            departmemt.append(eachdept)
        return departmemt
    
    total_department.short_description = "department"
    objects = UserManager()

    def __unicode__(self):
        return self.usertype

class TicketStatus(models.Model):
    statustype = models.CharField(max_length=30)

    def __unicode__(self):
        return self.statustype

class Team(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=250)
    landlineno = models.CharField(max_length=15)
    mobileno =  models.CharField(max_length=11)
    email = models.EmailField()

    def __unicode__(self):
        return self.name

class Customer(models.Model):
    company = models.CharField(max_length=50)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    landline = models.CharField(max_length=15)
    mobile = models.CharField(max_length=11)
    alternatemobile = models.CharField(max_length=11)
    email = models.EmailField()
    alternateemail = models.EmailField()

    def __unicode__(self):
        return self.company

class CustomerPackage(models.Model):
    package_type = models.CharField(max_length=50)

    def __unicode__(self):
        return self.package_type

class Sla(models.Model):
    slatype = models.CharField(max_length=50)

    def __unicode__(self):
        return self.slatype

class Dsk(models.Model):
    dsktype = models.CharField(max_length=50)

    def __unicode__(self):
        return self.dsktype

class Make(models.Model):
    make = models.CharField(max_length=50)

    def __unicode__(self):
        return self.make

class Ticket(models.Model):
    ts= models.DateTimeField()
    ticketid = models.CharField(max_length=30)
    customer = models.ForeignKey(Customer)
    make = models.ForeignKey(Make)
    summary = models.CharField(max_length=255)
    status = models.ForeignKey(TicketStatus)
    assignedto = models.ForeignKey(Team)
    priority = models.CharField(max_length=11)
    dept = models.ForeignKey(Deparment)
    sla = models.ForeignKey(Sla)
    attachment= models.FileField(upload_to=STATIC_PATH,blank=True,null=True)
    package = models.ForeignKey(CustomerPackage)

    def __unicode__(self):
        return self.ticketid