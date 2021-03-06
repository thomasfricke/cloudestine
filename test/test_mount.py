__author__ = 'thomas'

import sys

import unittest2 as unittest
import os
from logger import log
from cloudestine.mount import Mount
import random
from filecmp import cmp
from hashpath import HashPath

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

        os.system('rm -rf %s/* %s/*' %(rootdir,mountdir))
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
        self.assertFalse(self.mount.is_mounted())

    def test_mount_and_unmount(self):
        """
        tests the mount object
        :return:
        """
        self.assertTrue(self.mount.is_mounted())
        pass

    def test_write_to_mount_and_read_from_root(self):
        basename="testfile"

        mount_filename="%s/%s" % (self.mount.mountdir,basename)

        mount_file=file(mount_filename,"w+")

        value=random.random()
        mount_file.write("%f\n" % value)
        mount_file.close()

        self.assertTrue(os.path.exists(mount_filename))

        hashpath=HashPath("Salt")
        dir, full = hashpath.path("/"+basename,block=0)
        root_filename="%s/%s" % (self.mount.rootdir,full)

        self.assertTrue(cmp(root_filename,mount_filename))
        os.system("find test/rootdir test/mountdir -type f -ls")
        os.system("ls -lFt test")
        os.remove(mount_filename)
        self.assertFalse(os.path.exists(root_filename))



if __name__ == '__main__':
    unittest.main()
