from django.http import HttpResponse, HttpResponseBadRequest
from django.conf import settings
from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework import status


from NagiosParse import Nagios


class Comments(APIView):
    """
    Manage Comments

    Assign comments to Nagios host and service objects and remove comments
    from Nagios host and service objects

    """

    def put(self, request, *args, **kwargs):
        """
        Add a comment to a Nagios host or service object
        """

        OPTIONAL_FIELDS = {'service_description': None, 'author': 'nagios-api', 'persistent': 1}

        for i, j in OPTIONAL_FIELDS.items():
            if i not in kwargs:
                kwargs.update({i: j})

        inst = Nagios(settings.STATUS_FILE, settings.CMD_FILE)

        try:
            inst.add_comment(kwargs['hostname'], kwargs['comment'], kwargs['service_description'],
                             kwargs['author'], kwargs['persistent'])
        except:
            return Response('{"STATUS", "Unable to write to the Nagios command file"}', status=status.HTTP_404_NOT_FOUND, content_type='application/json')

        return Response('{"STATUS": "Comment added successfully"}', status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        """
        Delete comments from Nagios objects
        """

        OPTIONAL_FIELDS = {'service': False}

        for i, j in OPTIONAL_FIELDS.items():
            if i not in kwargs:
                kwargs.update({i: j})

        inst = Nagios(settings.STATUS_FILE, settings.CMD_FILE)

        try:
            if kwargs['service']:
                inst.remove_comment(kwargs['comment_id'], service=True)
            else:
                inst.remove_comment(kwargs['comment_id'])
        except:
            return Response('{"STATUS", "Unable to write to the Nagios command file"}', status=status.HTTP_404_NOT_FOUND, content_type='application/json')

        return Response('{"STATUS": "Comment removed successfully"}', status=status.HTTP_200_OK)


class Problems(APIView):
    """
    Display Service Problems

    """

    def get(self, request, *args, **kwargs):
        """
        Display the current service problems from status.dat
        """
        inst = Nagios(settings.STATUS_FILE, settings.CMD_FILE)

        return Response(inst.service_problems(), status=status.HTTP_200_OK)
