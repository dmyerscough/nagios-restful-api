#!/usr/bin/env python

import unittest
import os

class NagiosParseTest(unittest.TestCase):
    def setUp(self):
        self.valid = Nagios('tests/valid.dat')
        self.invalid = Nagios('tests/invalid.dat')

    def test_ParseStatus(self):
        """
        Test to make sure Parsing does occur
        """
        

    def test_missingBrace(self):
        """
        Parse an invalid cofiguration file
        """
        pass

    def test_missingStatus(self):
        """
        Try to read a status file that is missing
        """
        pass

    def test_queryMethod(self):
        """
        Check to see if the query method return a valid response
        and try query garbage
        """
        pass

    def test_hostMethod(self):
        """
        Test to see if the correct host is return when queried
        and the response to non-existant hosts
        """
        pass

    def test_allMethod(self):
        """
        Test to see if all hosts are returned
        """
        pass

if __name__ == '__main__':
    unittest.main()
