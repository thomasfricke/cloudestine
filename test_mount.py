__author__ = 'thomas'

import unittest2 as unittest
import sys, os
from xmp import main
from time import sleep
from logger import log

class Mount():

    def __init__(self):
        pass

class MountXMPCase(unittest.TestCase):

    def setUp(self):
        self.path   = os.path.dirname(os.path.realpath(__file__))
        self.module = "xmp.py"
        self.rootdir   = "%s/rootdir" % self.path
        self.mountdir  = "%s/mountdir" % self.path
        self.assertNotEqual(self.rootdir,self.mountdir)
        self.assertTrue(os.path.exists(self.rootdir))
        self.assertTrue(os.path.exists(self.mountdir))
        log.debug(sys.argv)


    def mount(self):
        return os.system("%s/%s -o root=%s %s" %(self.path, self.module, self.rootdir, self.mountdir))

    def tearDown(self):
        pass

    def unmount(self):
        print("fusermount -u %s" % self.mountdir)
        return os.system("fusermount -u %s" % self.mountdir)

    def wait_for_mount(self,mounted=True):
        for i in range(10):
            if self.is_mounted() == mounted:
                return True
            else:
                print("sleep for 1s")
                sleep(1)
        return False

    def test_mount_and_unmount(self):
        self.assertEqual(0,self.mount())
        self.assertTrue(self.wait_for_mount())
#        sleep(0)
        self.assertEqual(0,self.unmount())
        self.assertTrue(self.wait_for_mount(False))


    def is_mounted(self):

        proc_mount=file('/proc/mounts','r')
        for line in proc_mount.readlines():

            array=line.split(' ')
            if len(array)<3:
                continue
            (fs, mount_point, fuse)=array[0:3]
       #     print(array)
            if fs != self.module:
                continue

            if mount_point != self.mountdir:
                continue

            if fuse != 'fuse.%s' % self.module:
                continue


            log.debug("line=%s" % line)
            log.debug("array=%s" % array.__str__())

            return True

        return False

if __name__ == '__main__':
    unittest.main()
