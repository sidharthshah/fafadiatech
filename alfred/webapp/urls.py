from django.conf.urls.defaults import patterns, include, url

from django.contrib import admin
admin.autodiscover()
import os
STATIC_ROOT = os.path.join(os.path.dirname(os.path.realpath(__file__)),"static")
DOC_ROOT = os.path.join(STATIC_ROOT,"attachments")
FILE_ROOT = os.path.join(STATIC_ROOT,"attachments")
FILE_ROOT = FILE_ROOT[1:]+'/(?P<path>.*)$'

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'webapp.views.home', name='home'),
    # url(r'^webapp/', include('webapp.foo.urls')),
    url(FILE_ROOT, 'django.views.static.serve',{'document_root': DOC_ROOT, 'show_indexes': True}),
    url(r'^admin/', include(admin.site.urls)),
)
