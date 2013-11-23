'''
Created on 23.02.2013

@author: thomas
'''
import unittest2
import shutil
from .filename import FileName
import os
from .hashpath import HashPath

import logging

log=logging.getLogger(__name__)
logging.basicConfig(format='%(levelname)s:%(asctime)s:%(name)s:%(message)s',level=logging.DEBUG)

class FileTest(unittest2.TestCase):

    def __init__(self,test_name):
        super(FileTest, self).__init__(test_name)
        self.tmpdir = 'tmp'
     
    def setUp(self):
        pass
   
    def tearDown(self):
        shutil.rmtree(self.tmpdir) 
        pass
    
    def test_name(self):
        pass
        f=FileName(self.tmpdir,'dir/test')
        f.open('w')
        assert(os.path.isdir('tmp/dir'))
        assert(os.path.isfile('tmp/dir/test'))
        pass
    
    def test_makedirs_with_HashFileName_and_create_write_and_read_file(self):
  
        hashpath=HashPath("More Salt")
        log.debug("hashpath= %s" % hashpath)
        hashed_name=hashpath.path("finefile")
        filename=FileName(self.tmpdir,hashed_name)
        log.debug("hashed = %s" % filename.filename)
        filename.makedirs()
        log.debug("directory = %s" % filename.directory)
        assert(os.path.isdir(os.path.dirname(filename.directory)))
        
        f=filename.open('w')
        f.write("fine!")
        f.close()
        assert(os.path.isfile(filename.filename))
        
        f=filename.open()
        line=f.readline()
        f.close()
        
        assert( line == "fine!")
        pass
    

if __name__ == "__main__":
    unittest2.main()