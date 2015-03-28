#!/usr/bin/env python

# Copyright (C) 2001  Jeff Epler  <jepler@unpythonic.dhs.org>
#    Copyright (C) 2006  Csaba Henk  <csaba.henk@creo.hu>
#
#    This program can be distributed under the terms of the GNU LGPL.
#    See the file COPYING.
#

import os, sys
from errno import *
from stat import *
import fcntl
# pull in some spaghetti to make this stuff work without fuse-py being installed
try:
    import _find_fuse_parts
except ImportError:
    pass
import fuse
from fuse import Fuse
from logger import log
from hashpath import HashPath

if not hasattr(fuse, '__version__'):
    raise RuntimeError, \
        "your fuse-py doesn't know of fuse.__version__, probably it's too old."

fuse.fuse_python_api = (0, 2)

fuse.feature_assert('stateful_files', 'has_init')


def flag2mode(flags):
    md = {os.O_RDONLY: 'r', os.O_WRONLY: 'w', os.O_RDWR: 'w+'}
    m = md[flags & (os.O_RDONLY | os.O_WRONLY | os.O_RDWR)]

    if flags | os.O_APPEND:
        m = m.replace('w', 'a', 1)

    return m


class Xmp(Fuse):
    def __init__(self, *args, **kw):

        Fuse.__init__(self, *args, **kw)

        # do stuff to set up your filesystem here, if you want
        #import thread
        #thread.start_new_thread(self.mythread, ())
        self.root = '/'

    #    def mythread(self):
    #
    #        """
    #        The beauty of the FUSE python implementation is that with the python interp
    #        running in foreground, you can have threads
    #        """
    #        print "mythread: started"
    #        while 1:
    #            time.sleep(120)
    #            print "mythread: ticking"

    #
    # returns a posix.stat_result structure, initialises by a seqence
    #
    # s=posix.stat_result((33188,4050, 64513L, 1, 0, 0, 2324, 1414588643, 1414588643, 1414588643))
    # s
    # posix.stat_result(st_mode=33188, st_ino=4050, st_dev=64513L, st_nlink=1, st_uid=0,
    # st_gid=0, st_size=2324, st_atime=1414588643, st_mtime=1414588643, st_ctime=1414588643)
    #
    def getattr(self, path):
        log.debug("path %s" % path)
        lstat = os.lstat("." + path)
        hashpath=HashPath("Salt")
        lstat = os.lstat(hashpath.path(path))
        log.debug("lstat %s" % lstat)
        return lstat

    def readlink(self, path):
        log.debug("path %s" % path)
        rl = os.readlink("." + path)
        log.debug("readlink %s" % rl)
        return os.readlink("." + path)

    def readdir(self, path, offset):
        log.debug("path %s" % path)
        for e in os.listdir("." + path):
            yield fuse.Direntry(e)

    def unlink(self, path):
        log.debug("path %s" % path)
        os.unlink("." + path)
        hashpath=HashPath("Salt")
        dir, full = hashpath.path(path)
        os.unlink(full)
        self.unlink_empty_dirs(dir)

    def unlink_empty_dirs(self,dir):

        n=dir.rfind(os.path.sep)

        while True:
            try:
                log.debug("n=%d l=%d" %(n,len(dir)))
                os.rmdir(dir)
                log.debug(dir)
                if n == -1: break
            except OSError as ex:
                if ex.errno == ENOTEMPTY:
                    break
                else:
                    raise
            dir=dir[:n]
            n=dir.rfind(os.path.sep)


    def rmdir(self, path):
        log.debug("path %s" % path)
        os.rmdir("." + path)

    def symlink(self, path, path1):
        log.debug("path %s path1 %s" % (path, path1.__str__()))
        os.symlink(path, "." + path1)

    def rename(self, path, path1):
        log.debug("path %s path1 %s" % (path, path1.__str__()))
        os.rename("." + path, "." + path1)

    def link(self, path, path1):
        log.debug("path %s path1 %s" % (path, path1.__str__()))
        os.link("." + path, "." + path1)

    def chmod(self, path, mode):
        log.debug("path %s mode %d" % (path, mode))
        os.chmod("." + path, mode)

    def chown(self, path, user, group):
        log.debug("path %s user %d group %d" % (path, user, group ))
        os.chown("." + path, user, group)

    def truncate(self, path, len):
        log.debug("path %s len %d" % (path, len ))
        f = open("." + path, "a")
        f.truncate(len)
        f.close()

    def mknod(self, path, mode, dev):
        log.debug("path %s mode %d dev %d" % (path, dev ))
        os.mknod("." + path, mode, dev)

    def mkdir(self, path, mode):
        log.debug("path %s mode %d" % (path, mode))
        os.mkdir("." + path, mode)

    def utime(self, path, times):
        log.debug("path %s times %s" % (path, times))
        os.utime("." + path, times)

    #    The following utimens method would do the same as the above utime method.
    #    We can't make it better though as the Python stdlib doesn't know of
    #    subsecond preciseness in acces/modify times.
    #
    #    def utimens(self, path, ts_acc, ts_mod):
    #      os.utime("." + path, (ts_acc.tv_sec, ts_mod.tv_sec))

    def access(self, path, mode):
        log.debug("path %s mode %d" % ( path, mode))
        if not os.access("." + path, mode):
            return -EACCES

        #    This is how we could add stub extended attribute handlers...
        #    (We can't have ones which aptly delegate requests to the underlying fs
        #    because Python lacks a standard xattr interface.)
        #
        #    def getxattr(self, path, name, size):
        #        val = name.swapcase() + '@' + path
        #        if size == 0:
        #            # We are asked for size of the value.
        #            return len(val)
        #        return val
        #
        #    def listxattr(self, path, size):
        #        # We use the "user" namespace to please XFS utils
        #        aa = ["user." + a for a in ("foo", "bar")]
        #        if size == 0:
        #            # We are asked for size of the attr list, ie. joint size of attrs
        #            # plus null separators.
        #            return len("".join(aa)) + len(aa)
        #        return aa

    def statfs(self):
        """
        Should return an object with statvfs attributes (f_bsize, f_frsize...).
        Eg., the return value of os.statvfs() is such a thing (since py 2.2).
        If you are not reusing an existing statvfs object, start with
        fuse.StatVFS(), and define the attributes.

        To provide usable information (ie., you want sensible df(1)
        output, you are suggested to specify the following attributes:

            - f_bsize - preferred size of file blocks, in bytes
            - f_frsize - fundamental size of file blcoks, in bytes
                [if you have no idea, use the same as blocksize]
            - f_blocks - total number of blocks in the filesystem
            - f_bfree - number of free blocks
            - f_files - total number of file inodes
            - f_ffree - nunber of free file inodes
        """
        log.debug("statfs")

        return os.statvfs(".")

    def fsinit(self):
        log.debug("fsinit")
        os.chdir(self.root)

    class XmpFile(object):

        def __init__(self, path, flags, *mode):
            log.debug("file path %s flags %s mode %s " % ( path, flags, mode))
            self.file = os.fdopen(os.open("." + path, flags, *mode),
                                  flag2mode(flags))
            self.fd = self.file.fileno()

            log.debug("file %s fd %d" % (self.file, self.fd))

            self.path = path
            self.flags = flags

            self.direct_io = 0
            self.keep_cache = 0

            self.hashpath = HashPath("Salt")

        def read(self, length, offset):
            log.debug("file %s length %d offset %d mod %d" % (self.path, length, offset, offset % self.hashpath.block_size))
            dir, full = self.hashpath.path(self.path, block=offset)
            log.debug("hashpath %s/%s" % (dir,full))
#            log.debug("hashpath+%s/%s" % self.hashpath.path(self.path, block=offset + self.hashpath.block_size))
            hash_file=open(full)
            return hash_file.read(length)

            self.file.seek(offset)
            return self.file.read(length)

        def write(self, buf, offset):
            log.debug("file %s length of buf %d offset %d mod %d" % (self.path, len(buf), offset, offset % self.hashpath.block_size))
            dir, full = self.hashpath.path(self.path, block=offset)
            log.debug("hashpath %s %s" % (dir,full))
            try:
                try:
                    os.makedirs(dir)
                except OSError as exception:
                    if exception.errno != EEXIST or not os.path.isdir(dir):
                        raise

                log.debug("dir created")
                hash_file=open(full,"w")
                hash_file.write(buf)
                hash_file.close()
            except IOError as ex:
                log.error("could not write data" % ex.message)

            self.file.seek(offset)
            self.file.write(buf)
            return len(buf)

        def release(self, flags):
            log.debug("file %s flags %d\n" % (self.path, flags))
            self.file.close()

        def _fflush(self):
            log.debug("file %s" % self.path)
            if 'w' in self.file.mode or 'a' in self.file.mode:
                self.file.flush()

        def fsync(self, isfsyncfile):
            log.debug("file %s isfsyncfile %d" % (self.path, isfsyncfile))
            self._fflush()
            if isfsyncfile and hasattr(os, 'fdatasync'):
                os.fdatasync(self.fd)
            else:
                os.fsync(self.fd)

        def flush(self):
            log.debug("file %s" % self.path)
            self._fflush()
            # cf. xmp_flush() in fusexmp_fh.c
            os.close(os.dup(self.fd))

        def fgetattr(self):
            log.debug("file %s" % self.path)
            return os.fstat(self.fd)

        def ftruncate(self, len):
            log.debug("file %s len %d" % ( self.path, len))
            self.file.truncate(len)

        def lock(self, cmd, owner, **kw):
            # The code here is much rather just a demonstration of the locking
            # API than something which actually was seen to be useful.

            # Advisory file locking is pretty messy in Unix, and the Python
            # interface to this doesn't make it better.
            # We can't do fcntl(2)/F_GETLK from Python in a platfrom independent
            # way. The following implementation *might* work under Linux. 
            #
            # if cmd == fcntl.F_GETLK:
            #     import struct
            # 
            #     lockdata = struct.pack('hhQQi', kw['l_type'], os.SEEK_SET,
            #                            kw['l_start'], kw['l_len'], kw['l_pid'])
            #     ld2 = fcntl.fcntl(self.fd, fcntl.F_GETLK, lockdata)
            #     flockfields = ('l_type', 'l_whence', 'l_start', 'l_len', 'l_pid')
            #     uld2 = struct.unpack('hhQQi', ld2)
            #     res = {}
            #     for i in xrange(len(uld2)):
            #          res[flockfields[i]] = uld2[i]
            #  
            #     return fuse.Flock(**res)

            # Convert fcntl-ish lock parameters to Python's weird
            # lockf(3)/flock(2) medley locking API...
            op = {fcntl.F_UNLCK: fcntl.LOCK_UN,
                  fcntl.F_RDLCK: fcntl.LOCK_SH,
                  fcntl.F_WRLCK: fcntl.LOCK_EX}[kw['l_type']]
            if cmd == fcntl.F_GETLK:
                return -EOPNOTSUPP
            elif cmd == fcntl.F_SETLK:
                if op != fcntl.LOCK_UN:
                    op |= fcntl.LOCK_NB
            elif cmd == fcntl.F_SETLKW:
                pass
            else:
                return -EINVAL

            fcntl.lockf(self.fd, op, kw['l_start'], kw['l_len'])


    def main(self, *a, **kw):

        self.file_class = self.XmpFile

        return Fuse.main(self, *a, **kw)


def main():
    usage = """
Userspace nullfs-alike: mirror the filesystem tree from some point on.

""" + Fuse.fusage

    server = Xmp(version="%prog " + fuse.__version__,
                 usage=usage,
                 dash_s_do='setsingle')

    # Disable multithreading: if you want to use it, protect all method of
    # XmlFile class with locks, in order to prevent race conditions
    server.multithreaded = False

    server.parser.add_option(mountopt="root", metavar="PATH", default='/',
                             help="mirror filesystem from under PATH [default: %default]")
    server.parse(values=server, errex=1)

    try:
        if server.fuse_args.mount_expected():
            os.chdir(server.root)
    except OSError:
        print >> sys.stderr, "can't enter root of underlying filesystem"
        sys.exit(1)

    server.main()


if __name__ == '__main__':
    main()
