__author__ = 'thomas'

import sys

import unittest2 as unittest
import os
from logger import log
from cloudestine.mount import Mount


class MountXMPCase(unittest.TestCase):

    def setUp(self):
        """
        create a Mount object to be tested
        :return:
        """
        path   = os.path.dirname(os.path.realpath(__file__))

        module = "xmp.py"
        rootdir   = "%s/rootdir" % path
        mountdir  = "%s/mountdir" % path

        self.mount=Mount( path, module, rootdir, mountdir)

        self.assertNotEqual(self.mount.rootdir,self.mount.mountdir)
        self.assertTrue(os.path.exists(self.mount.rootdir))
        self.assertTrue(os.path.exists(self.mount.mountdir))
        log.debug(sys.argv)

    def test_mount_and_unmount(self):
        """
        tests the mount object
        :return:
        """
        self.assertEqual(0,self.mount.mount())
        self.assertTrue(self.mount.wait_for_mount())

        self.assertEqual(0,self.mount.unmount())
        self.assertTrue(self.mount.wait_for_mount(False))

if __name__ == '__main__':
    unittest.main()
