# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from settings import ROOT_PATH
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'common.views.main_Page'),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': ROOT_PATH+'/media'}),
    url(r'^searchPage/$', 'knowledge.views.searchPage'),
)