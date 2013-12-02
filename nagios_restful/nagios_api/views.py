from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.conf import settings

from NagiosParse import Nagios


def add_comment(request, hostname, comment, service_description=None, author='nagios-api', persistent=1):
    inst = Nagios(settings.STATUS_FILE, settings.CMD_FILE)

    try:
        inst.add_comment(hostname, comment, service_description, author, persistent)
    except:
        return HttpResponseBadRequest('Unable to write to the Nagios command file')
 
    return HttpResponse('{"STATUS": "Comment added successfully"}', content_type='application/json')

def remove_comment(request, comment_id, service=None):
    inst = Nagios(settings.STATUS_FILE, settings.CMD_FILE)

    try:
        if service:
            inst.remove_comment(comment_id, service=True)
        else:
            inst.remove_comment(comment_id)

    except:
        return HttpResponseBadRequest('Unable to write to the Nagios command file')

    return HttpResponse('{"STATUS": "Comment removed successfully"}', content_type='application/json')


def problems(request):
    """
    Display the current service problems from status.dat

    """
    inst = Nagios(settings.STATUS_FILE, settings.CMD_FILE)

    return HttpResponse(inst.service_problems(as_json=True), content_type='application/json')
