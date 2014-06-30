from django.conf.urls import url, patterns, include
from django.contrib import admin
from django.views.generic import TemplateView
from django.shortcuts import render


admin.autodiscover()

#def my_view(request):
#    return render(request, get_ab_template(request, 'page.html'))

#http://stackoverflow.com/questions/15059519/what-is-equivalent-of-direct-to-template-in-class-based-view-in-django
urlpatterns = patterns(
    '',
    url(r'^$',include('chopauth.urls')),
    url(r'', include('chopauth.urls')),
    url(r'^dashboard/{0,1}$', 'mybic.views.dashboard', name='dashboard'),
    url(r'^accounts/login/{0,1}$', 'mybic.views.dashboard', name='dashboard'),
    url(r'^/{0,1}$', 'mybic.views.dashboard', name='dashboard'),

    #url(r'^page/$', my_view, name='my-page'),
    # Administrative components
    url(r'^admin/', include(admin.site.urls)),
    url(r'^labs/(\w+)/$', 'mybic.labs.views.labview', name='my_lab_url'),
    url(r'^labs/(\w+)/(\w+)/$', 'mybic.labs.views.projectview', name='my_project_url'),

    #url(r'^labs/', include('mybic.labs.urls')),
    #url(r'^labs/(\S+)$', 'mybic.views.labs'),
)

#url(r'^$', TemplateView.as_view(template_name='index.html')),
#url(r'^accounts/login/{0,1}$', TemplateView.as_view(template_name='foo_index.html'))