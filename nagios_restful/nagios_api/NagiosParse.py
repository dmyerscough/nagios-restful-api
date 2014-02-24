#!/usr/bin/env python

import json
import time

__author__ = 'Damian Myerscough'


class Nagios:
    """
    Nagios v3 and v4 Parser
    """

    def __init__(self, config, statusFile=None):
        self.config = config
        self.server = {}
        self.hosts = {}
        self.misc = {}

        self.problem_hosts = {}

        self.statusFile = statusFile

        self._Parse()

    def host(self, hostname, is_json=False):
        """
        Return a single host that the user requested

        :param hostname
               The hostname that the user would like to query

        :param json
               Have the hosts have all the values return in a
               json format

        """
        if is_json:
            return self.hosts[hostname]
        else:
            return self.server[hostname]

    def all(self, is_json=False):
        """
        Return all the hosts in json format

        :param json
               Return all hosts in json format

        """
        if is_json:
            return self.hosts
        else:
            return self.server

    def service_problems(self, as_json=False):
        """
        Return a list of hosts that have problems
        """
        for host, service in self.server.items():
            if hasattr(service, 'servicestatus'):
                for i in service.servicestatus.keys():
                    if (int(self.server[host].servicestatus[i].
                            get('current_state')) != 0 and
                        int(self.server[host].servicestatus[i].
                            get('current_attempt')) ==
                        int(self.server[host].servicestatus[i].
                            get('max_attempts'))):
                        if self.problem_hosts.get(host, 0):
                            (self.problem_hosts[host]['servicestatus'].
                             update({i: self.server[host].servicestatus[i]}))
                        else:
                            self.problem_hosts[host] = ({'servicestatus':
                                                        {i: self.server[host].
                                                            servicestatus[i]}})

        if as_json:
            return self.problem_hosts
        else:
            return self.problem_hosts

    def query(self, block_def):
        """
        Allow the user to query other Nagios definitions

        :param block
               The Nagios block definition

        """
        return self.misc[block_def]

    def _Parse(self):
        """
        Parse the Nagios status file
        """

        service_type = None
        hostname = None
        service = None
        parse = False

        try:
            fh = open(self.config, 'r')
        except IOError as e:
            raise Exception("Unable to open {0}".format(self.config))

        for line in fh.readlines():
            if line.strip().endswith('{'):
                if parse:
                    raise Exception('Found open brace before closing brace')
                parse = True
                service_type = line.strip().split(' ')[0]
                continue
            elif line.strip().endswith('}'):
                if hostname:
                    self.server[hostname] = NagiosHost(self.hosts[hostname])

                hostname = service = None
                parse = False
                continue

            if parse:
                key, value = line.strip().split('=', 1)

                if key == 'host_name' or key == 'servicecomment':
                    hostname = value
                    continue
                elif key == 'service_description':
                    if hostname:
                        service = value
                        continue
                    else:
                        raise Exception('service_description before host_name')

                if hostname:
                    if service:
                        if (self.hosts[hostname].get(service_type, 0)
                            and self.hosts[hostname][service_type].
                                get(service, 0)):

                            (self.hosts[hostname][service_type][service].
                             update({key: value}))
                        else:
                            if self.hosts[hostname].get(service_type, 0):
                                (self.hosts[hostname][service_type].
                                 update({service: {key: value}}))
                            else:
                                (self.hosts[hostname].
                                 update({service_type: {service:
                                        {key: value}}}))
                    else:
                        if self.hosts.get(hostname, 0):
                            self.hosts[hostname].update({key: value})
                        else:
                            self.hosts[hostname] = {key: value}
                else:
                    if self.misc.get(service_type, 0):
                        self.misc[service_type].update({key: value})
                    else:
                        self.misc.update({service_type: {key: value}})

    def acknowledge_problem(self, hostname, comment, service_description=None,
                            author='nagios-api', persistent=1, notify=1,
                            sticky=2):
        """
        Ackowledge service or host problems

        :param hostname
               The hostname to acknowledge the problem

        :param comment
               The comment to be applied to the problem

        :param author
               The user who would like to perform this action, this will allow
               other users know who acknowledged the problem

        :param persistent
               If persistent is set to one, the comment associated with
               the acknowledgement will survive across restarts of the
               Nagios process.

        :param notify
               If the notify is set to one, a notification will be sent out
               to contacts indicating that the current host problem has been
               acknowledged.

        :param sticky
               If the sticky is set to two, the acknowledgement will remain
               until the host returns to an UP state.

        :param service_description
               The name of the service that will be acknowledged

        """
        if service_description:
            cmd = ("ACKNOWLEDGE_SVC_PROBLEM;{0};{1};{2};{3};{4};{5};{6};{7}".
                   format(hostname, service_description, sticky, notify,
                          persistent, author, comment))
        else:
            cmd = ("ACKNOWLEDGE_HOST_PROBLEM;{0};{1};{2};{3};{4};{5}".
                   format(hostname, sticky, notify, persistent,
                          author, comment))

        with open(self.statusFile, 'a') as fh:
            fh.write('[{0}] {1}\n'.format(int(time.time()), cmd))

    def remove_acknowledgement(self, hostname, service_description=None):
        """
        Remove acknowledgements from hosts or services

        :param hostname
               The hostname you would like the acknowledgement removed from

        :param service_description
               The service name that you would like to remove the
               acknowledgment from

        """
        if service_description:
            cmd = ("REMOVE_SVC_ACKNOWLEDGEMENT;{0};{1}".
                   format(hostname, service_description))
        else:
            cmd = "REMOVE_HOST_ACKNOWLEDGEMENT;{0}".format(hostname)

        with open(self.statusFile, 'a') as fh:
            fh.write('[{0}] {1}\n'.format(int(time.time()), cmd))

        return True

    def add_comment(self, hostname, comment, service_description=None,
                    author='nagios-api', persistent=1):
        """
        Add comments to hosts and services

        :param hostname
               The hostname to apply the comment to

        :param comment
               The comment to be shown on the service or host

        :param author
               The username to be visable in the Nagios web interface

        :param persistent
                If the persistent field is set to zero (0), the comment will be
                deleted the next time Nagios is restarted. If persistent is set
                to one the comment will persist across program restarts until
                it is deleted manually.

        :param service_description
               The service description that you want to apply a comment to

        """
        if service_description:
            cmd = ("ADD_SVC_COMMENT;{0};{1};{2};{3};{4}".
                   format(hostname, service_description,
                          persistent, author, comment))
        else:
            cmd = ("ADD_HOST_COMMENT;{0};{1};{2};{3}".
                   format(hostname, persistent, author, comment))

        with open(self.statusFile, 'a') as fh:
            fh.write('[{0}] {1}\n'.format(int(time.time()), cmd))

        return True

    def remove_comment(self, comment_id, service=None):
        """
        Remove a host or service comment

        :param comment_id
               The comment ID that will be removed

        :param service
               Remove the comment from a service

        """
        if service:
            cmd = "DEL_SVC_COMMENT;{0}".format(comment_id)
        else:
            cmd = "DEL_HOST_COMMENT;{0}".format(comment_id)

        with open(self.statusFile, 'a') as fh:
            fh.write('[{0}] {1}\n'.format(int(time.time()), cmd))

        return True

    def schedule_downtime(self, hostname, comment, start_time, end_time,
                          duration, service_description=None,
                          author='nagios-api', fixed=0, trigger_id=0):
        """
        Schedule downtime for a host or service

        :param hostname
               The hostname to schedule downtime for

        :param comment
               Present a comment in the Nagios web interface

        :param service_description
               The name of the service to schedule downtime for

        :param start_time
               The start_time argument specifies in time_t format
               (seconds since the UNIX epoch) for the maintenance to being

        :param end_time
               The end_time argument specifies in time_t format
               (seconds since the UNIX epoch) for the maintenance to end

        :param fixed
               The specified service downtime can be triggered by another
               downtime entry

        :param trigger_id
               Set argument to zero if the downtime for the specified
               host/service should not be triggered by another downtime entry

        :param duration
               How long the downtime will last in seconds

        :param author
               The user who would like to perform this action, this will allow
               other users know who acknowledged the problem

        """
        if service_description:
            cmd = ("SCHEDULE_SVC_DOWNTIME;{0};{1};{2};{3};{4};{5};{6};{7};{8}".
                   format(hostname, service_description, start_time, end_time,
                          fixed, trigger_id, duration, author, comment))
        else:
            cmd = ("SCHEDULE_HOST_DOWNTIME;{0};{1};{2};{3};{4};{5};{6};{7}".
                   format(hostname, start_time, end_time, fixed, trigger_id,
                          duration, author, comment))

        with open(self.statusFile, 'a') as fh:
            fh.write('[{0}] {1}\n'.format(int(time.time()), cmd))

        return True

    def cancel_downtime(self, hostname, downtime_id, service=None):
        """
        Cancel downtime for a host or service

        :param hostname
               The hostname you would like to cancel the downtime

        :param downtime_id
               The downtime ID to remove

        :param service
               If the downtime needs to be removed from a service

        """
        if service:
            cmd = "DEL_SVC_DOWNTIME;{0}".format(downtime_id)
        else:
            cmd = "DEL_HOST_DOWNTIME;{0}".format(downtime_id)

        with open(self.statusFile, 'a') as fh:
            fh.write('[{0}] {1}\n'.format(int(time.time()), cmd))

        return True

    def enable_notifications(self, hostname, service_description=None):
        """
        Enable notifications for a host or service

        :param hostname
               The hostname to enable notifications

        :param service_description
               The service description to enable notifications

        """
        if service_description:
            cmd = ("ENABLE_SVC_NOTIFICATIONS;{0};{1}".
                   format(hostname, service_description))
        else:
            cmd = "ENABLE_HOST_NOTIFICATIONS;{0}".format(hostname)

        with open(self.statusFile, 'a') as fh:
            fh.write('[{0}] {1}\n'.format(int(time.time()), cmd))

        return True

    def disable_notifications(self, hostname, service_description=None):
        """
        Disable notifications for a host or service

        :param hostname
               The hostname to disable notifications

        :param service_description
               The service description to disable notifications

        """
        if service_description:
            cmd = ("DISABLE_SVC_NOTIFICATIONS;{0};{1}".
                   format(hostname, service_description))
        else:
            cmd = "DISABLE_HOST_NOTIFICATIONS;{0}".format(hostname)

        with open(self.statusFile, 'a') as fh:
            fh.write('[{0}] {1}\n'.format(int(time.time()), cmd))

        return True

    def schedule_check(self, hostname, check_time, service_description=None):
        """
        Schedule a host or service check

        :param hostname
               The hostname to schedule the check against

        :param check_time
               The "check_time" argument is specified in time_t format
               (seconds since the UNIX epoch)

        :param service_description
               Service name to perform a check against

        """
        if service_description:
            cmd = "SCHEDULE_SVC_CHECK;{0};{1};{2}".format(hostname,
                                                          service_description,
                                                          check_time)
        else:
            cmd = "SCHEDULE_HOST_CHECK;{0};{1}".format(hostname, check_time)

        with open(self.statusFile, 'a') as fh:
            fh.write('[{0}] {1}\n'.format(int(time.time()), cmd))

        return True


class NagiosHost:
    """
    Nagios Host Systems
    """
    def __init__(self, obj):
        self.__dict__.update(obj)


if __name__ == '__main__':

    n = Nagios('../../../status.dat')
    print n.service_problems(True)
    #for host, service in  n.host('example.com').servicestatus.items():
    #    print host, service.get('current_state')

    #print n.host('example.com', True)
    #print n.query('info').keys()
