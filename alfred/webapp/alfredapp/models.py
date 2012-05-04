from django.db import models
from django.contrib.auth.models import User, UserManager

class Deparment(models.Model):
    department = models.CharField(max_length=30)

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
     
     
class TicketStatus(models.Model):
    statustype = models.CharField(max_length=30)
    
class Team(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=250)
    landline = models.CharField(max_length=15)
    mobile =  models.CharField(max_length=11)
    email = models.EmailField()
    
class Customer(models.Model):
    company = models.CharField(max_length=50)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    landline = models.CharField(max_length=15)
    mobile = models.CharField(max_length=11)
    email = models.EmailField()

class CustomerPackage(models.Model):
    package_type = models.CharField(max_length=50)

class Sla(models.Model):
    slatype = models.CharField(max_length=50)

class Dsk(models.Model):
    dsktype = models.CharField(max_length=50)
    
class Make(models.Model):
    make = models.CharField(max_length=50)


    