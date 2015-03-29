__author__ = 'thomas'

import os
from logger import log
from time import sleep

class Mount():

    def __init__(self,path,module,rootdir,mountdir):
        self.path = path
        self.module = module
        self.rootdir   = rootdir
        self.mountdir  = mountdir
        pass

    def mount(self,retry=3):
        if self.is_mounted(): return 0
        for i in range(retry):
            result = os.system("%s/%s -o root=%s %s" %(self.path, self.module, self.rootdir, self.mountdir))
            if result:
                log.debug("mount failed, unmount")
                sleep(1)
                self.unmount()
                sleep(1)
            else:
                return 0
        return result

    def unmount(self,retry=3):

        if not self.is_mounted(): return 0

        for i in range(retry):
            result = os.system("fusermount -u %s" % self.mountdir)
            if result:
                log.debug("ummount failed, repeat")
                sleep(1)
            else:
                return 0

        return result

    def wait_for_mount(self,mounted=True):
        for i in range(100):
            if self.is_mounted() == mounted:
                return True
            else:
                log.debug("sleep for 1s")
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
