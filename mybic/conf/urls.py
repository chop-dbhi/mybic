from django.conf.urls import url, patterns, include
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView
from django.shortcuts import render
from haystack.forms import SearchForm
from haystack.forms import ModelSearchForm
from haystack.query import SearchQuerySet
from haystack.views import SearchView
from mybic.labs.models import Project
from news.models import Article
from django.conf import settings

admin.autodiscover()

sqs = SearchQuerySet().models(Project,Article)
#.filter(lab__slug='Pei_lab')


urlpatterns = patterns(
    '',
    url(r'^$',include('chopauth.urls')),
    url(r'', include('chopauth.urls')),

    url(r'^news/$', 'mybic.views.news', name='news'),

    url(r'^admin/', include(admin.site.urls)),
    
    url(r'^toggle/', 'mybic.views.masquerade', name='toggle_url'),
    
    url(r'^accounts/login/{0,1}$', 'mybic.views.dashboard', name='dashboard'),
    url(r'^dashboard/{0,1}$', 'mybic.views.dashboard', name='dashboard'),
    url(r'^/{0,1}$', 'mybic.views.dashboard', name='dashboard'),

    # Administrative components
    
    url(r'^labs/$','mybic.views.dashboard', name='dashboard'),
    url(r'^labs/([\w-]+)/$', 'mybic.labs.views.labview', name='my_lab_url'),
    url(r'^labs/([\w-]+)/([\w-]+)/$', 'mybic.labs.views.projectview', name='my_project_url'),

    url(r'^search', SearchView(
        template='search/search.html',
        searchqueryset=sqs,
        form_class=ModelSearchForm
    ), name='haystack_search'),

    url(r'^labs/([\w-]+)/([\w-]+)/(.+)$', 'mybic.labs.views.childview', name='my_child_url'),
    
    url(r'^update/([\w-]+)/([\w-]+)/$', 'mybic.labs.views.updateproject', name='update_project_url'),
    url(r'^slink/(?P<lab>[\w-]+)/(?P<project>[\w-]+)/(?P<path>.+)$','mybic.views.protected_file',name='protected')

) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

#'haystack.views',
#url(r'^search/', include('haystack.urls')),
