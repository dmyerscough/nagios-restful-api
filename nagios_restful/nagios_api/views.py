from django.http import HttpResponse, HttpResponseBadRequest
from django.conf import settings
from django.shortcuts import render
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from NagiosParse import Nagios


class Comments(View):
    """
    Manage Comments - Assign comments to Nagios host and service objects and remove comments
                      from Nagios host and service objects

    """

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(Comments, self).dispatch(*args, **kwargs)

    def put(self, request, *args, **kwargs):
        """
        Add a comment to a Nagios host or service object
        """

        OPTIONAL_FIELDS = {'service_description': None, 'author': 'nagios-api', 'persistent': 1}

        for i, j in OPTIONAL_FIELDS.items():
            if not kwargs.has_key(i):
                kwargs.update({i: j})

        inst = Nagios(settings.STATUS_FILE, settings.CMD_FILE)

        try:
            inst.add_comment(kwargs['hostname'], kwargs['comment'], kwargs['service_description'],
                             kwargs['author'], kwargs['persistent'])
        except:
            return HttpResponseBadRequest('Unable to write to the Nagios command file')
 
        return HttpResponse('{"STATUS": "Comment added successfully"}', content_type='application/json')


    def delete(self, request, *args, **kwargs):
        """
        Delete comments from Nagios objects
        """

        OPTIONAL_FIELDS = {'service': False}

        for i, j in OPTIONAL_FIELDS.items():
            if not kwargs.has_key(i):
                kwargs.update({i: j})

        inst = Nagios(settings.STATUS_FILE, settings.CMD_FILE)

        try:
            if kwargs['service']:
                inst.remove_comment(kwargs['comment_id'], service=True)
            else:
                inst.remove_comment(kwargs['comment_id'])
        except:
            return HttpResponseBadRequest('Unable to write to the Nagios command file')

        return HttpResponse('{"STATUS": "Comment removed successfully"}', content_type='application/json')


def problems(request):
    """
    Display the current service problems from status.dat

    """
    inst = Nagios(settings.STATUS_FILE, settings.CMD_FILE)

    return HttpResponse(inst.service_problems(as_json=True), content_type='application/json')
