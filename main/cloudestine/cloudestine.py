#!/usr/bin/env python
'''
Created on 12.02.2013

@author: thomas
'''


import getopt
import os
import sys
import logging
from fuse import FUSE, Operations, LoggingMixIn
from getopt import GetoptError
from io.hashpath import HashPath
from stat import S_IFREG, S_IFDIR

log=logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
logging.basicConfig(format='%(levelname)s:%(asctime)s:%(name)s:%(funcName)s:%(lineno)d:%(message)s',
                    level=logging.DEBUG)

class Cloudestine(LoggingMixIn, Operations):

    def __init__(self, verbose, mount,base_name,gnupghome='~/.cloudestine/gpg',
                 hashpath=HashPath('Salt'),hash_split=4,blocksize=1024 ) :
        self.verbose = verbose
        self.mount = mount
        if not os.path.isdir(self.mount):
            msg="directory %s does not exist" % (__name__,self.mount)
            log.error(msg)
            raise Exception(msg)
                            
        self.base_name = base_name
        self.gnupghome = gnupghome 
        self.hashpath = hashpath
        self.blocksize = blocksize
        self.fd=0
        pass
    
    """
    helper function to compute the dirname
    """
    def storage_directory(self,path):
        return os.path.dirname( self.base_name + os.path.sep+path )
    """
    helper function to compute the filename
    """
    def storage_filename(self,path):
        return self.base_name+os.path.sep+path
    
    """
    helper function for write operations, creates all necessary directories
    """
    def filename_create_dirs_for_path_and_block(self,path,block=0):
        hashedpath=self.hashpath.path(path,block=block)
        directory = self.storage_directory(hashedpath)
        filename = self.storage_filename(hashedpath)
        log.debug("hp: %s, dir: %s, f: %s" %(hashedpath,directory,filename))
        if not os.path.isdir(directory):
            if not os.path.exists(directory):
                os.makedirs(directory) 
        return filename
    
    def readdir(self, path, fh):
        log.debug("readdir: %s" % path)
        hashedpath=self.hashpath.path(path,block=0)
        filename = self.storage_filename(hashedpath)

        dirents = ['.', '..']
        if os.path.isdir(filename):
            dirents.extend(os.listdir(filename))
        for r in dirents:
            yield r
    """
    helper function to turn integer flags into string
    """
    def flag2mode(self,flags):
        md = {os.O_RDONLY: 'r', os.O_WRONLY: 'w', os.O_RDWR: 'w+'}
        m = md[flags & (os.O_RDONLY | os.O_WRONLY | os.O_RDWR)]

        if flags | os.O_APPEND:
            m = m.replace('w', 'a', 1)
       
        return m

    """
    open a file
    """
    def open(self, path, mode):
        log.debug("open: %s" % path)
        filename=self.filename_create_dirs_for_path_and_block(path)
        log.debug("map to %s, mode %d, flag2mode %s" % ( filename, mode, self.flag2mode(mode)))
        fh=open(filename,self.flag2mode(mode))
        log.debug("fh %s" % fh.__str__())
        return fh.fileno()
        self.fd+=1
        return self.fd
    """
    create a file, delegating to open
    """
    def create(self,path,mode):
        log.debug("create: %s" % path)
        return self.open(path, mode | os.O_WRONLY | os.O_CREAT)
    
    def statfs(self, path):
        log.debug("path=%s" %path)
        hashedpath=self.hashpath.path(path,block=0)
        filename = self.storage_filename(hashedpath)
        #stv = os.statvfs(filename)
        stv = os.statvfs('/etc/passwd')
        return dict((key, getattr(stv, key)) for key in ('f_bavail', 'f_bfree',
            'f_blocks', 'f_bsize', 'f_favail', 'f_ffree', 'f_files', 'f_flag',
            'f_frsize', 'f_namemax'))
    
    def getattr(self, path, fh=None):
        log.debug("path=%s" % path)
        if path=="/":
            return dict(st_mode=(S_IFDIR | 0755), st_nlink=2)
        else:
            return dict(st_mode=(S_IFREG | 0755), st_nlink=2)
        
    def flush(self, path, fh):
        return os.fsync(fh)

    def fsync(self, path, datasync, fh):
        return os.fsync(fh)
    
    def write(self, path, data, offset, fh):
        log.debug("write %s data %s offset %d fh %d" % (path, data, offset, fh))
#        block = offset / self.blocksize
#        hashfile_offset = offset % self.blocksize
        
        filename=self.filename_create_dirs_for_path_and_block(path)     
        log.debug("filename %s" % filename)    
        f=open(filename,'a')
        f.write(data)
        log.debug("data %s" % data)
        return len(data)
    
      
    @classmethod    
    def usage(clazz):
        print """
    usage:
      %s mount base
    """ % os.path.basename(sys.argv[0])
        pass

    @classmethod
    def main(clazz,sys_argv=sys.argv[1:]):
        try:
            opts, args = getopt.getopt(sys_argv, "cfg:hum#:", 
                                       ["help","foreground=",
                                        "hash-algorithm=",
                                        "gnupg-home=","create","--unmount"])
        
        except getopt.GetoptError as err:
            # print help information and exit:
            print str(err) # will print something like "option -a not recognized"
            Cloudestine.usage()
            sys.exit(2)
        
        verbose = False
        foreground = False
        create = False
        unmount = False
        gnupghome='~/.cloudestine/gpg'
        mount = args[0]
                   
        for o, a in opts:
            if o == "-v":
                verbose = True
            elif o in ("-h", "--help"):
                Cloudestine.usage()
                sys.exit()
            elif o in ("-m", "--mount"):
                mount = a
            elif o in ("-f","--foreground"):
                foreground=True
            elif o in ("-f","--gnupg-home"):
                gnupghome=a
            elif o in ("-c", "--create" ):
                create = True
            elif o in ("-u", "--unmount" ):
                unmount=True
            else:
                assert False, "unhandled option"
        
        if unmount:
            exit ( os.system("fusermount -u %s" % mount ) )
        
        
        if len(args) <2:
            log.error( "args: %s" % args.__str__())
            log.error( "opts: %s" % args.__str__())
            raise GetoptError("mount or base_name path missing")
        elif len(args)>3:
            raise GetoptError("extra args not allowed")    
        base_name = args[1]
        
        
        for p in ( mount, base_name ): 
            if not os.path.isdir(p):
                if create:
                    os.makedirs(p)
                else:
                    print "%s path does not exist or is not a directory" % p
                    sys.exit(1)
       
            
        cloudestine=Cloudestine(verbose=verbose,
                                mount = mount,
                                base_name = base_name,
                                gnupghome=gnupghome,
                                )
         
        FUSE( cloudestine, mount, foreground=foreground)

if __name__ == "__main__":
    Cloudestine.main()