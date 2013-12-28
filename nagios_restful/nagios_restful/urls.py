from django.conf.urls import patterns, include, url

from nagios_api.views import Comments, Problems, Notifications, ScheduleChecks, Downtime


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

    # Manage host and service notifications
    url('^notification/(?P<hostname>[-a-zA-Z0-9]+)/$', Notifications.as_view()),
    url('^notification/(?P<hostname>[-a-zA-Z0-9]+)/(?P<service>[-a-zA-Z0-9_]+)/$', Notifications.as_view()),

    # Schedule host or service checks
    url('^schedule/check/(?P<hostname>[-a-zA-Z0-9]+)/$', ScheduleChecks.as_view()),
    url('^schedule/check/(?P<hostname>[-a-zA-Z0-9]+)/(?P<service>[-a-zA-Z0-9_]+)/$', ScheduleChecks.as_view()),

    # Schedule and cancel downtime
    url('^downtime/(?P<hostname>[-a-zA-Z0-9]+)/(?P<comment>[-a-zA-Z0-9 _]+)/(?P<start>[0-9]{10,15})/(?P<finish>[0-9]{10,15})/(?P<author>[-a-zA-Z0-9 _]+)/$', Downtime.as_view()),
    url('^downtime/(?P<hostname>[-a-zA-Z0-9]+)/(?P<comment>[-a-zA-Z0-9 _]+)/(?P<start>[0-9]{10,15})/(?P<finish>[0-9]{10,15})/(?P<service>[-a-zA-Z0-9_]+)/(?P<author>[-a-zA-Z0-9 _]+)/$', Downtime.as_view()),
)
