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

log=logging.getLogger(__name__)

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
        pass
    
    """
    helper function to compute the dirname
    """
    def storage_directory(self,path):
        return os.path.dirname( self.base_name + os.path.pathsep+path )
    """
    helper function to compute the filename
    """
    def storage_filename(self,path):
        return self.base_name+os.path.pathsep+path
    
    """
    helper function for write operations, creates all necessary directories
    """
    def filename_create_dirs_for_path_and_block(self,path,block=0):
        hashedpath=self.hashpath.path(path,block=block)
        directory = self.storage_directory(hashedpath)
        filename = self.storage_filename(hashedpath)
        
        if not os.path.isdir(directory):
            if not os.path.exists(directory):
                os.makedirs(directory) 
        return filename
    
    """
    open a file
    """
    def open(self, path, mode):
        log.debug("open: %s" + path)
        filename=self.filename_create_dirs_for_path_and_block(path)
        return os.open(filename, mode)
    """
    create a file, delegating to open
    """
    def create(self,path,mode):
        return self.open(path, mode | os.O_WRONLY | os.O_CREAT)
    
    def flush(self, path, fh):
        return os.fsync(fh)

    def fsync(self, path, datasync, fh):
        return os.fsync(fh)
    
    def write(self, path, data, offset, fh):
        block = offset / self.blocksize
        hashfile_offset = offset % self.blocksize
        
        filename=self.filename_create_dirs_for_path_and_block(path)         
        f=open(filename)
        f.write(data)
        print data
        return len(data)
    
    @classmethod    
    def usage():
        print """
    usage:
      %s path
    """ % os.path.basename(sys.argv[0])
        pass

    @classmethod
    def main(clazz,sys_argv=sys.argv[1:]):
        try:
            opts, args = getopt.getopt(sys_argv, "fg:hm#:", 
                                       ["help","foreground=",
                                        "hash-algorithm=",
                                        "gnupg-home="])
            if len(args) <2:
                raise GetoptError("mount or base_name path missing")
            elif len(args)>3:
                raise GetoptError("extra args not allowed")
        except getopt.GetoptError as err:
            # print help information and exit:
            print str(err) # will print something like "option -a not recognized"
            Cloudestine.usage()
            sys.exit(2)
        
        verbose = False
        foreground = False
        gnupghome='~/.cloudestine/gpg'
        mount = args[0]
        base_name = args[1]
           
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
            else:
                assert False, "unhandled option"
        
      
        for pair in ( ("mount", mount),("base_name", base_name) ): 
            if not os.path.isdir(mount):
                print "%s path %s does not exist or is not a directory" % pair
                sys.exit(1)
       
            
        cloudestine=Cloudestine(verbose=verbose,
                                mount = mount,
                                base_name = base_name,
                                gnupghome=gnupghome,
                                )
         
        FUSE( cloudestine, mount, foreground=foreground)

if __name__ == "__main__":
    Cloudestine.main()