'''
Created on 12.02.2013

@author: thomas
'''
#!/usr/bin/env python

import getopt
import os
import sys

from fuse import FUSE, Operations, LoggingMixIn
from getopt import GetoptError
from io.hashpath import HashPath


class Cloudestine(LoggingMixIn, Operations):

    def __init__(self, mount,storage,verbose,gnupghome='~/.cloudestine/gpg',
                 hash_algorithm='sha1',hash_split=4 ) :
        self.verbose = verbose
        self.mount = mount
        self.storage = storage
        self.gnupghome = gnupghome 
        self.hashpath = HashPath("",hash_algorithm,split_num=hash_split)
        pass
    
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
                raise GetoptError("mount or storage path missing")
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
        storage = args[1]
        hash_algorithm = 'sha1'
        
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
            elif o in ("-#","--hash-algorithm"):
                hash_algorithm = a
            else:
                assert False, "unhandled option"
        
      
        for pair in ( ("mount", mount),("storage", storage) ): 
            if not os.path.isdir(mount):
                print "%s path %s does not exist or is not a directory" % pair
                sys.exit(1)
       
            
        cloudestine=Cloudestine(mount,storage,gnupghome=gnupghome,
                                verbose=verbose,hash_algorithm=hash_algorithm)
         
        FUSE( cloudestine, mount, foreground=foreground)

if __name__ == "__main__":
    Cloudestine.main()