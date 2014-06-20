from django.conf.urls import url, patterns, include
from django.contrib import admin
from django.views.generic import TemplateView
from django.shortcuts import render

from django.views.generic.simple import direct_to_template

admin.autodiscover()

#def my_view(request):
#    return render(request, get_ab_template(request, 'page.html'))


urlpatterns = patterns(
    '',
    url(r'', include('chopauth.urls')),
    #url(r'^page/$', my_view, name='my-page'),
    # Administrative components
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/login/{0,1}$', direct_to_template, {'template': 'foo_index.html'}
)


