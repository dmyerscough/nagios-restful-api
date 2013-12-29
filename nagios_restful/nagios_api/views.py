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
        inst = Nagios(settings.STATUS_FILE, settings.CMD_FILE)

        try:
            inst.add_comment(kwargs['hostname'], kwargs['comment'],
                             kwargs.get('service_description', None),
                             kwargs.get('author', 'nagios-api'),
                             kwargs.get('persistent', 1))
        except:
            return Response('''{"STATUS",
                            "Unable to write to the Nagios command file"}''',
                            status=status.HTTP_404_NOT_FOUND,
                            content_type='application/json')

        return Response('{"STATUS": "Comment added successfully"}',
                        status=status.HTTP_200_OK,
                        content_type='application/json')

    def delete(self, request, *args, **kwargs):
        """
        Delete comments from Nagios objects
        """
        inst = Nagios(settings.STATUS_FILE, settings.CMD_FILE)

        try:
            inst.remove_comment(kwargs['comment_id'],
                                kwargs.get('service', False))
        except:
            return Response('''{"STATUS",
                            "Unable to write to the Nagios command file"}''',
                            status=status.HTTP_404_NOT_FOUND,
                            content_type='application/json')

        return Response('{"STATUS": "Comment removed successfully"}',
                        status=status.HTTP_200_OK,
                        content_type='application/json')


class Notifications(APIView):
    """
    Manage Nagios Notifications
    """

    def put(self, request, *args, **kwargs):
        """
        Enable Notifications for either Hosts or host services
        """
        inst = Nagios(settings.STATUS_FILE, settings.CMD_FILE)

        try:
            inst.enable_notifications(kwargs['hostname'],
                                      kwargs.get('service', None))
        except:
            return Response('''{"STATUS",
                            "Unable to write to the Nagios command file"}''',
                            status=status.HTTP_404_NOT_FOUND,
                            content_type='application/json')

        return Response('{"STATUS": "Notification enabled"}',
                        status=status.HTTP_200_OK,
                        content_type='application/json')

    def delete(self, request, *args, **kwargs):
        """
        Disable Nagios Notifications for either Host or service
        """
        inst = Nagios(settings.STATUS_FILE, settings.CMD_FILE)

        try:
            inst.disable_notifications(kwargs['hostname'],
                                       kwargs.get('service', None))
        except:
            return Response('''{"STATUS",
                            "Unable to write to the Nagios command file"}''',
                            status=status.HTTP_404_NOT_FOUND,
                            content_type='application/json')

        return Response('{"STATUS": "Notification disabled"}',
                        status=status.HTTP_200_OK,
                        content_type='application/json')


class ScheduleChecks(APIView):
    """
    Manage scheduled checks
    """

    def put(self, request, *args, **kwargs):
        """
        Allow users to schedule checks
        """
        inst = Nagios(settings.STATUS_FILE, settings.CMD_FILE)

        try:
            inst.schedule_check(kwargs['hostname'], kwargs['time'],
                                kwargs.get('service', None))
        except:
            return Response('''{"STATUS",
                            "Unable to write to the Nagios command file"}''',
                            status=status.HTTP_404_NOT_FOUND,
                            content_type='application/json')

        return Response('{"STATUS": "Check scheduled successfully"}',
                        status=status.HTTP_200_OK,
                        content_type='application/json')


class Downtime(APIView):
    """
    Manage scheduled downtime
    """

    def put(self, request, *args, **kwargs):
        """
        Allow users to schedule downtime
        """
        inst = Nagios(settings.STATUS_FILE, settings.CMD_FILE)

        try:
            inst.schedule_downtime(kwargs['hostname'], kwargs['comment'],
                                   kwargs['start'], kwargs['finish'],
                                   kwargs['finish'] - kwargs['start'],
                                   kwargs.get('service', None),
                                   kwargs.get('author', None))
        except:
            return Response('''{"STATUS",
                            "Unable to write to the Nagios command file"}''',
                            status=status.HTTP_404_NOT_FOUND,
                            content_type='application/json')

        return Response('{"STATUS": "Downtime scheduled"}',
                        status=status.HTTP_200_OK,
                        content_type='application/json')

    def delete(self, request, *args, **kwargs):
        """
        Cancel scheduled downtime
        """
        inst = Nagios(settings.STATUS_FILE, settings.CMD_FILE)

        try:
            inst.cancel_downtime(kwargs['hostname'], kwargs['downtime_id'],
                                 kwargs.get('service', None))
        except:
            return Response('''{"STATUS",
                            "Unable to write to the Nagios command file"}''',
                            status=status.HTTP_404_NOT_FOUND,
                            content_type='application/json')

        return Response('{"STATUS": "Downtime cancelled"}',
                        status=status.HTTP_200_OK,
                        content_type='application/json')


class Problems(APIView):
    """
    Display Service Problems
    """

    def get(self, request, *args, **kwargs):
        """
        Display the current service problems from status.dat
        """
        inst = Nagios(settings.STATUS_FILE, settings.CMD_FILE)

        return Response(inst.service_problems(),
                        status=status.HTTP_200_OK,
                        content_type='application/json')


class HostStatus(APIView):
    """
    Display overall host status
    """

    def get(self, request, *args, **kwargs):
        """
        View the status of an individual host
        """
        inst = Nagios(settings.STATUS_FILE, settings.CMD_FILE)

        try:
            return Response(inst.host(kwargs['hostname'], True),
                            status=status.HTTP_200_OK,
                            content_type='application/json')
        except KeyError:
            return Response('{"STATUS": "Hostname does not exist"}',
                            status=status.HTTP_200_OK,
                            content_type='application/json')


class AllHosts(APIView):
    """
    Dump All Hosts
    """

    def get(self, request, *args, **kwargs):
        """
        Display all hosts and all services
        """
        inst = Nagios(settings.STATUS_FILE, settings.CMD_FILE)

        return Response(inst.all(True),
                        status=status.HTTP_200_OK,
                        content_type='application/json')
