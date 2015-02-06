from django.conf.urls import patterns, url

from mybic.labs import views

import news

urlpatterns = patterns('',
                       url(r'^$', views.index, name='index')
)


