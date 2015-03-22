__author__ = 'thomas'

import os
from logger import log
class Mount():

    def __init__(self,path,module,rootdir,mountdir):
        self.path = path
        self.module = module
        self.rootdir   = rootdir
        self.mountdir  = mountdir
        pass

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
