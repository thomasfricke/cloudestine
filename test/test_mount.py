__author__ = 'thomas'

import sys

import unittest2 as unittest
import os
from logger import log
from cloudestine.mount import Mount
import random
from filecmp import cmp

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

        self.assertEqual(0,self.mount.mount())
        self.assertTrue(self.mount.wait_for_mount())

    def tearDown(self):
        self.assertEqual(0,self.mount.unmount())
        self.assertTrue(self.mount.wait_for_mount(False))

    def test_mount_and_unmount(self):
        """
        tests the mount object
        :return:
        """
        pass



    def test_write_to_root_and_read_from_mount(self):
        basename="testfile"
        root_filename="%s/%s" % (self.mount.rootdir,basename)
        mount_filename="%s/%s" % (self.mount.mountdir,basename)

        root_file=file(root_filename,"w+")

        value=random.random()
        root_file.write("%f\n" % value)
        root_file.close()

        self.assertTrue(cmp(root_filename,mount_filename))

        os.remove(root_filename)

        self.assertFalse(os._exists(mount_filename))

    def test_write_to_mount_and_read_from_root(self):
        basename="testfile"
        root_filename="%s/%s" % (self.mount.rootdir,basename)
        mount_filename="%s/%s" % (self.mount.mountdir,basename)

        mount_file=file(mount_filename,"w+")

        value=random.random()
        mount_file.write("%f\n" % value)
        mount_file.close()

        self.assertTrue(cmp(root_filename,mount_filename))

        os.remove(mount_filename)
        self.assertFalse(os._exists(root_filename))



if __name__ == '__main__':
    unittest.main()
