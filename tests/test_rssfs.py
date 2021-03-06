from __future__ import absolute_import
from __future__ import unicode_literals

import unittest




import collections
from datetime import datetime
import io
import itertools
import json
import math
import os
import time
import fs
import fs.copy
import fs.move
from fs import ResourceType, Seek
from fs import errors
from fs import walk
from fs.opener import open_fs
from fs.subfs import ClosingSubFS, SubFS

import pytz
import six
from six import text_type
from fs.rssfs import *
#~ import rssfs 

class TestRSSFS(unittest.TestCase):


    def make_fs(self):
        # Return an instance of your FS object here
        url = 'http://planetpython.org/rss20.xml'
        self.url = url

        return RSSFS(url)


    def destroy_fs(self, fs):
        """
        Destroy a FS object.

        :param fs: A FS instance previously opened by
            `~fs.test.FSTestCases.make_fs`.

        """
        fs.close()

    def setUp(self):
        self.fs = self.make_fs()

    def tearDown(self):
        self.destroy_fs(self.fs)
        del self.fs
        
    def test_root(self):
        assert self.fs.listdir(u'/') == ['Planet Python']
        assert self.fs.isdir(u'/')
        
        assert self.fs.listdir(u'/Planet Python')
        assert self.fs.isdir(u'/Planet Python')
        
    def test_getinfo(self):
        
        info = self.fs.getinfo(u'/').raw
        self.assertIsInstance(info['basic']['name'], text_type)
        # ~ self.assertEqual(info['basic']['name'], '')
        self.assertTrue(info['basic']['is_dir'])
        
        info = self.fs.getinfo(u'/Planet Python').raw
        self.assertIsInstance(info['basic']['name'], text_type)
        # ~ self.assertEqual(info['basic']['name'], '')
        self.assertTrue(info['basic']['is_dir'])
        
        testfile = self.fs.listdir(u'/Planet Python')[0]
        # ~ print (testfile)
        
        info = self.fs.getinfo(u'/Planet Python/%s'%testfile).raw
        self.assertIsInstance(info['basic']['name'], text_type)
        self.assertEqual(info['basic']['name'], testfile)
        self.assertFalse(info['basic']['is_dir'])
        
        fo = self.fs.open(u'/Planet Python/%s'%testfile)
        # ~ print (repr(fo.read()))






# ~ def run():
    # ~ unittest.main()

# ~ if __name__ == '__main__':
    # ~ unittest.main()
