from django.conf.urls import url, patterns, include
from django.contrib import admin
from django.views.generic import TemplateView
from django.shortcuts import render

admin.autodiscover()

#def my_view(request):
#    return render(request, get_ab_template(request, 'page.html'))


urlpatterns = patterns(
    '',
    #url(r'^page/$', my_view, name='my-page'),
    # Administrative components
    url(r'^admin/', include(admin.site.urls)),
)


