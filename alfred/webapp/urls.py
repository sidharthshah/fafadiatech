from django.conf.urls.defaults import patterns, include, url
from alfredapp.views import *
from django.contrib import admin

admin.autodiscover()
import os
STATIC_ROOT = os.path.join(os.path.dirname(os.path.realpath(__file__)),"static")
DOC_ROOT = os.path.join(STATIC_ROOT,"attachments")
FILE_ROOT = os.path.join(STATIC_ROOT,"attachments")
FILE_ROOT = FILE_ROOT[1:]+'/(?P<path>.*)$'

urlpatterns = patterns('',
    # Examples:
    url(r'^user/dashboard', 'alfredapp.views.userdashboard'),
    url(r'^customer/summary', 'alfredapp.views.customersummary'),
    url(r'^customer/create', 'alfredapp.views.customeradd'),
    url(r'^customer/add', 'alfredapp.views.customeraddpost'),
    url(r'^customer/modify', 'alfredapp.views.customeredit'),
    url(r'^customer/edit', 'alfredapp.views.customermodify'),
    url(r'^user/add', 'alfredapp.views.useradd'),
    url(r'^user/edit','alfredapp.views.usereditform'),
    url(r'^user/modify','alfredapp.views.modifyuser'),
    url(r'^user/delete','alfredapp.views.deleteuser'),
    url(r'^team/dashboard','alfredapp.views.teamdashboard'),
    url(FILE_ROOT, 'django.views.static.serve',{'document_root': DOC_ROOT, 'show_indexes': True}),
    url(r'^admin/', include(admin.site.urls)),
    
)
