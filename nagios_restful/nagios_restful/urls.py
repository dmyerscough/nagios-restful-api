from django.conf.urls import patterns, include, url

urlpatterns = patterns('',

    url('^problems/$', 'nagios_api.views.problems'),

    url('^comment/(?P<hostname>[-a-zA-Z0-9]+)/(?P<comment>[-a-zA-Z0-9 _]+)/$', 'nagios_api.views.add_comment'),
    url('^comment/(?P<hostname>[-a-zA-Z0-9]+)/(?P<comment>[-a-zA-Z0-9 _]+)/(?P<service_description>[-a-zA-Z0-9_]+)/$', 'nagios_api.views.add_comment'),
    url('^comment/(?P<hostname>[-a-zA-Z0-9]+)/(?P<comment>[-a-zA-Z0-9 _]+)/(?P<service_description>[-a-zA-Z0-9_]+)/(?P<author>[a-zA-Z0-9]+)/$', 'nagios_api.views.add_comment'),
    url('^comment/(?P<hostname>[-a-zA-Z0-9]+)/(?P<comment>[-a-zA-Z0-9 _]+)/(?P<service_description>[-a-zA-Z0-9_]+)/(?P<author>[a-zA-Z0-9]+)?/(?P<persistent>\d{1})/$', 'nagios_api.views.add_comment'),

    url('^comment/(?P<comment_id>\d{1,5})/$', 'nagios_api.views.remove_comment'),
    url('^comment/(?P<comment_id>\d{1,5})/(?P<service>[true|false])/$', 'nagios_api.views.remove_comment'),
)
