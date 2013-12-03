from django.conf.urls import patterns, include, url

from nagios_api.views import Comments, Problems


urlpatterns = patterns('',

    url('^problems/$', Problems.as_view()),

    #url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),


    url('^comment/(?P<comment_id>\d{1,5})/$', Comments.as_view()),
    url('^comment/(?P<comment_id>\d{1,5})/(?P<service>\d{1,5})/$', Comments.as_view()),

    url('^comment/(?P<hostname>[-a-zA-Z0-9]+)/(?P<comment>[-a-zA-Z0-9 _]+)/$', Comments.as_view()),
    url('^comment/(?P<hostname>[-a-zA-Z0-9]+)/(?P<comment>[-a-zA-Z0-9 _]+)/$', Comments.as_view()),
    url('^comment/(?P<hostname>[-a-zA-Z0-9]+)/(?P<comment>[-a-zA-Z0-9 _]+)/(?P<service_description>[-a-zA-Z0-9_]+)/$', Comments.as_view()),
    url('^comment/(?P<hostname>[-a-zA-Z0-9]+)/(?P<comment>[-a-zA-Z0-9 _]+)/(?P<service_description>[-a-zA-Z0-9_]+)/(?P<author>[a-zA-Z0-9]+)/$', Comments.as_view()),
    url('^comment/(?P<hostname>[-a-zA-Z0-9]+)/(?P<comment>[-a-zA-Z0-9 _]+)/(?P<service_description>[-a-zA-Z0-9_]+)/(?P<author>[a-zA-Z0-9]+)?/(?P<persistent>\d{1})/$', Comments.as_view()),


)
