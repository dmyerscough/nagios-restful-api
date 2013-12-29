#!/usr/bin/env python


import unittest

from NagiosParse import Nagios


class NagiosParseTest(unittest.TestCase):

    def setUp(self):
        self.valid = Nagios('tests/valid.dat', 'nagios.cmd')
        self.host_block = []

        fh = open('tests/host_options')
        for i in fh.readlines():
            self.host_block.append(i.strip())

        """
        Append the servicestatus block definition since this
        holds service states
        """
        self.host_block.append('servicestatus')

    def test_ParseStatus(self):
        """
        Test to make sure Parsing does occur
        """
        methods = ([i for i in dir(self.valid.host('example.com'))
                    if not i.startswith('__')])

        self.assertEqual(tuple(sorted(methods)),
                         tuple(sorted(self.host_block)))

    def test_missingBrace(self):
        """
        Parse an invalid cofiguration file
        """
        self.assertRaises(Exception, Nagios, 'tests/invalid.dat')

    def test_missingStatus(self):
        """
        Try to read a status file that is missing
        """
        self.assertRaises(Exception, Nagios, 'tests/blah.dat')

    def test_queryMethod(self):
        """
        Check to see if the query method return a valid response
        and try query garbage
        """
        methods = ['update_available', 'new_version', 'created',
                   'last_update_check', 'last_version', 'version']

        self.assertEqual(tuple(sorted(methods)),
                         tuple(sorted(self.valid.query('info'))))

    def test_hostMethod(self):
        """
        Test to see if the correct host is return when queried
        and the response to non-existant hosts
        """
        service_keys = ['DISK_USR', 'DISK_VAR', 'DISK_HOME', 'DISK_BOOT']
        methods = ([i for i in dir(self.valid.host('example.com'))
                    if not i.startswith('__')])

        self.assertEqual(tuple(sorted(methods)),
                         tuple(sorted(self.host_block)))
        self.assertEqual(sorted(self.valid.host('example.com').
                                servicestatus.keys()), sorted(service_keys))

    def test_allMethod(self):
        """
        Test to see if all hosts are returned
        """
        self.assertEquals(tuple(self.valid.all().keys()), ('example.com',))

if __name__ == '__main__':
    unittest.main()
