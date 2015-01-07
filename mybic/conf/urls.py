from django.conf.urls import url, patterns, include
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView
from django.shortcuts import render

from django.conf import settings

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$',include('chopauth.urls')),
    url(r'', include('chopauth.urls')),
    
    url(r'^admin/', include(admin.site.urls)),
    
    url(r'^accounts/login/{0,1}$', 'mybic.views.dashboard', name='dashboard'),
    url(r'^dashboard/{0,1}$', 'mybic.views.dashboard', name='dashboard'),
    url(r'^/{0,1}$', 'mybic.views.dashboard', name='dashboard'),

    # Administrative components
    
    url(r'^labs/$','mybic.views.dashboard', name='dashboard'),
    url(r'^labs/([\w-]+)/$', 'mybic.labs.views.labview', name='my_lab_url'),
    url(r'^labs/([\w-]+)/([\w-]+)/$', 'mybic.labs.views.projectview', name='my_project_url'),

    url(r'^slink/(?P<lab>[\w-]+)/(?P<project>[\w-]+)/(?P<path>.+)$','mybic.views.protected_file',name='protected')
    
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

