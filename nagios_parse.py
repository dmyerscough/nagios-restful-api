#!/usr/bin/env python



class Nagios:
    """

    """

    def __init__(self, config):
        self.nagios = ['hoststatus', 'servicestatus', 'servicecomment']
        self.config = config

        self.hosts = {}

        self._Parse()

    def host(self, hostname):
        """

        """
        return self.hosts[hostname]

    def all(self):
        """

        """
        return self.hosts

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
                hostname = service = None
                parse = False
                continue

            if parse:
                try:
                    key, value = line.strip().split('=', 1)
                except:
                    import pdb;pdb.set_trace() 

                if key == 'host_name':
                    hostname = value
                    continue
                elif key == 'service_description':
                    service = value
                    continue

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


if __name__ == '__main__':

    n = Nagios('../status.dat')
    print n.host('ops-nbmedia1-1-sfm')
