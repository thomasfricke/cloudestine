'''
Created on 12.02.2013

@author: thomas
'''
#!/usr/bin/env python

from __future__ import with_statement

import getopt
import os
import sys

from fuse import FUSE, FuseOSError, Operations, LoggingMixIn
from getopt import GetoptError


class Cloudestine(LoggingMixIn, Operations):
    
    def __init__(self, verbose, mount ) :
        self.verbose = verbose
        self.mount = mount
        pass
           
def usage():
  print """
usage:
  %s path
""" % os.path.basename(sys.argv[0])
  pass

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hfm:", ["help"])
        if len(args) == 0:
            raise GetoptError("mount path missing")
        elif len(args)>1:
            raise GetoptError("multiple mount paths not allowed")
    except getopt.GetoptError as err:
        # print help information and exit:
        print str(err) # will print something like "option -a not recognized"
        usage()
        sys.exit(2)
    
    verbose=False
    foreground=False
    mount = args[0]
    
    for o, a in opts:
        if o == "-v":
            verbose = True
        elif o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-m", "--mount"):
            mount = a
        elif o in ("-f","--forground"):
            foreground=True
        else:
            assert False, "unhandled option"
    
    cloudestine=Cloudestine(mount,verbose)
     
    fuse = FUSE( cloudestine, foreground=foreground)

if __name__ == "__main__":
    main()