from django.conf.urls import url, patterns, include
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView
from django.shortcuts import render
from haystack.forms import SearchForm
from haystack.forms import ModelSearchForm
from haystack.query import SearchQuerySet
from haystack.views import SearchView
from mybic.labs.models import Project, ProjectFile, ProtectedFile
from news.models import Article
from django.conf import settings

admin.autodiscover()

sqs = SearchQuerySet().models(Project, Article, ProjectFile, ProtectedFile)

from haystack.forms import ModelSearchForm, HighlightedModelSearchForm

urlpatterns = patterns(
    '',
    url(r'^$', include('chopauth.urls')),
    url(r'', include('chopauth.urls')),


    url(r'^news/{0,1}$', 'mybic.views.news', name='news'),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^tracking/', include('tracking.urls')),
    url(r'^toggle/{0,1}$', 'mybic.views.masquerade', name='toggle_url'),

    url(r'^accounts/login/{0,1}$', 'mybic.views.dashboard', name='dashboard'),
    url(r'^dashboard/{0,1}$', 'mybic.views.dashboard', name='dashboard'),
    url(r'^/{0,1}$', 'mybic.views.dashboard', name='dashboard'),

    # Administrative components

    url(r'^labs/{0,1}$', 'mybic.views.dashboard', name='dashboard'),
    url(r'^labs/([\w-]+)/{0,1}$', 'mybic.labs.views.labview', name='my_lab_url'),
    url(r'^labs/([\w-]+)/([\w-]+)/$', 'mybic.labs.views.projectview', name='my_project_url'),

    # Project Endpoint
    url(r'^api/([\w-]+)/([\w-]+)/{0,1}$', 'mybic.labs.views.projectendpoint', name='project_endpoint'),

    url(r'^logs/([\w-]+)/([\w-]+)/{0,1}$', 'mybic.labs.views.project_logs', name='project_logs'),


    url(r'^labs/([\w-]+)/([\w-]+)/(.+)$', 'mybic.labs.views.childview', name='my_child_url'),
    url(r'^labs/(.+)$', 'mybic.labs.views.childview', name='my_direct_child_url'),

    url(r'^update/([\w-]+)/([\w-]+)/{0,1}$', 'mybic.labs.views.updateproject', name='update_project_url'),

    url(r'^new/{0,1}$', 'mybic.labs.views.upload_project_fixture', name='upload_project_fixture_url'),

    url(r'^slink/(?P<lab>[\w-]+)/(?P<project>[\w-]+)/(?P<path>.+)/{0,1}$', 'mybic.views.protected_file', name='protected'),


    url(r'^search', SearchView(
        template='search/search.html',
        
        form_class=HighlightedModelSearchForm,
    ), name='haystack_search')

) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

#'haystack.views',
#url(r'^search/', include('haystack.urls')),
