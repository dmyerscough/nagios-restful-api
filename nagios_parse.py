#!/usr/bin/env python

import json

class Nagios:
    """
    Nagios status.dat parser
    """

    def __init__(self, config):
        self.config = config
        self.server = {}
        self.misc = {}

        self.hosts = {}

        self._Parse()

    def host(self, hostname):
        """
        Return the users request hostname
        """
        return self.server[hostname]

    def all(self):
        """
        Return all the hosts
        """
        return self.hosts

    def query(self, block):
        """

        """
        try:
            return self.misc[block]
        except:
            return False

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
                        if self.hosts[hostname].get(service_type, 0) and self.hosts[hostname][service_type].get(service, 0):
                            self.hosts[hostname][service_type][service].update({key: value})
                        else:
                            if self.hosts[hostname].get(service_type, 0):
                                self.hosts[hostname][service_type].update({service: {key: value}})
                            else:
                                self.hosts[hostname].update({service_type: {service: {key: value}}})
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

class NagiosHost:
    """
    Nagios Host Systems
    """
    def __init__(self, obj):
        self.__dict__.update(obj)

if __name__ == '__main__':

    n = Nagios('../status.dat')
    print n.host('ops-nbmedia1-1-sfm').problem_has_been_acknowledged
    #print json.dumps({'ops.nbmedia1-1-sfm': n.host('ops-nbmedia1-1-sfm')})
    #print n.query('info').keys()
