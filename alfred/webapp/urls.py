from django.conf.urls.defaults import patterns, include, url
from alfredapp.views import *
from django.contrib import admin
import os
admin.autodiscover()

STATIC_ROOT = os.path.join(os.path.dirname(os.path.realpath(__file__)),"static")
DOC_ROOT = os.path.join(STATIC_ROOT,"attachments")
FILE_ROOT = os.path.join(STATIC_ROOT,"attachments")
FILE_ROOT = FILE_ROOT[1:]+'/(?P<path>.*)$'

urlpatterns = patterns('',
    url(r'^$','alfredapp.views.home'),
    url(r'^login','alfredapp.views.login'),
    url(r'^dashboard','alfredapp.views.dashboard'),
    url(r'^user/dashboard', 'alfredapp.views.userdashboard'),
    url(r'^user/edit', 'alfredapp.views.useredit'),
    url(r'^customer/dashboard','alfredapp.views.customerdashboard'),
    url(r'^customer/ticketdisplayinfo','alfredapp.views.customerdisplayticket'),
    url(r'^customer/summary', 'alfredapp.views.customersummary'),
    url(r'^customer/displayticketstatuswise','alfredapp.views.customerdisplayticketbystatus'),
    url(r'^customer/edit','alfredapp.views.customeredit'),
    url(r'^customer/ticketcreateform','alfredapp.views.createcustomerTicketform'),
    url(r'^customer/ticketcreate','alfredapp.views.createcustomerTicket'),
    url(r'^customer/create', 'alfredapp.views.customeradd'),
    url(r'^customer/add', 'alfredapp.views.customeraddpost'),
    url(r'^customer/edit', 'alfredapp.views.customeredit'),
    url(r'^customer/modify', 'alfredapp.views.customermodify'),
    url(r'^customer/delete', 'alfredapp.views.deletecustomer'),
#    url(r'^user/add', 'alfredapp.views.useradd'),
#    url(r'^user/edit','alfredapp.views.usereditform'),
#    url(r'^user/modify','alfredapp.views.modifyuser'),
#    url(r'^user/delete','alfredapp.views.deleteuser'),
    url(r'^employee/dashboard','alfredapp.views.employeedashboard'),
    url(r'^team/ticketcreateform','alfredapp.views.createteamTicketform'),
    url(r'^team/ticketcreate','alfredapp.views.createteamTicket'),
    url(r'^team/dashboard','alfredapp.views.teamdashboard'),
    url(r'^team/displayticketstatuswise','alfredapp.views.teamdisplayticketbystatus'),
    url(r'^team/addform', 'alfredapp.views.addteamform'),
    url(r'^team/add', 'alfredapp.views.teamadd'),
    url(r'^team/edit','alfredapp.views.teameditform'),
    url(r'^team/modify','alfredapp.views.modifyteam'),
    url(r'^team/delete','alfredapp.views.deleteteam'),
    url(r'^department/dashbard','alfredapp.views.departmentdashboard'),
    url(r'^department/add','alfredapp.views.departmentadd'),
    url(r'^department/edit','alfredapp.views.departmentedit'),
    url(r'^department/modify','alfredapp.views.departmentmodify'),
    url(r'^department/delete','alfredapp.views.deletedepartment'),
    url(r'^customerpackage/dashboard','alfredapp.views.customerpackagedashboard'),
    url(r'^customerpackage/add','alfredapp.views.customerpackageadd'),
    url(r'^customerpackage/edit','alfredapp.views.customerpackageedit'),
    url(r'^customerpackage/modify','alfredapp.views.customerpackagemodify'),
    url(r'^customerpackage/delete','alfredapp.views.customerpackagedelete'),
    url(r'^sla/dashboard','alfredapp.views.sladashboard'),
    url(r'^sla/add','alfredapp.views.slaadd'),
    url(r'^sla/edit','alfredapp.views.slaedit'),
    url(r'^sla/modify','alfredapp.views.slamodify'),
    url(r'^sla/delete','alfredapp.views.sladelete'),
    url(r'^ticketstatus/dashboard','alfredapp.views.ticketstatusdashboard'),
    url(r'^ticketstatus/add','alfredapp.views.ticketstatusadd'),
    url(r'^ticketstatus/edit','alfredapp.views.ticketstatusedit'),
    url(r'^ticketstatus/modify','alfredapp.views.ticketstatusmodify'),
    url(r'^ticketstatus/delete','alfredapp.views.ticketstatusdelete'),
    url(r'^ticket/create','alfredapp.views.createticketform'),
    url(r'^ticket/add','alfredapp.views.createticket'),
    url(r'^customer/displaydata','alfredapp.views.dispcustomerdata'),
    url(r'^ticket/assign','alfredapp.views.ticketassign'),
    url(r'^ticket/delete','alfredapp.views.deleteticket'),
    url(r'^ticket/getdetailsbyticketid','alfredapp.views.getdetailsbyticketid'),
    url(r'^ticket/statusassign','alfredapp.views.ticketstatusassign'),
    #url(r'^sadmin/status','alfredapp.views.ticketassign'),
    url(r'^departmentadmin/dashboard','alfredapp.views.departmentadmindashboard'),
    url(r'^departmentadmin/ticketcreate','alfredapp.views.departmentadmincreateticket'),
    url(r'^employee/allticket','alfredapp.views.employeeallticket'),
    url(r'^employee/ticketdetails','alfredapp.views.employeeticketdetails'),
    url(r'^ticket/sadmin/status','alfredapp.views.sadminticketstatus'),
    url(r'^ticket/displayedit','alfredapp.views.ticketdisplayinfo'),
    url(r'^admin/ticket/assign/edit','alfredapp.views.departmentticketdisplay'),
    url(r'^ticket/departmentassign','alfredapp.views.assignticketdepartment'),
    url(r'^ticket/memberassign','alfredapp.views.assignticketmember'),
    url(r'^ticket/slaassign','alfredapp.views.assignticketsla'),
    #url(r'^ticket/assign/modify','alfredapp.views.ticketassignmodify'),
    url(r'^ticket/by_customername','alfredapp.views.get_all_ticket_by_customername'),
    url(r'^ticket/by_companyname','alfredapp.views.get_all_ticket_by_companyname'),
    url(r'^ticket/by_departmentname','alfredapp.views.get_all_ticket_by_departmentname'),
    url(r'^ticket/by_assignedname','alfredapp.views.get_all_ticket_by_assignedname'),
    url(r'^ticket/by_statusname','alfredapp.views.get_all_ticket_by_statusname'),
    url(r'^adminreport/allticket','alfredapp.views.admin_get_all_ticket_report'),
    url(r'^adminreport/by_customer','alfredapp.views.admin_by_customer_report'),
    url(r'^adminreport/feedback','alfredapp.views.admin_feedback_report'),
    #url(r'^report/allticket','alfredapp.views.reports_all_ticket'),
    url(r'^search/', include('haystack.urls')),
    url(FILE_ROOT, 'django.views.static.serve',{'document_root': DOC_ROOT, 'show_indexes': True}),
    url(r'^admin/', include(admin.site.urls)),
    
)
