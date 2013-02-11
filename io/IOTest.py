#!/usr/bin/env python 

import unittest
from io.HashPath import HashPath

class Hashtest(unittest.TestCase):

    def setUp(self):
        self.hash = HashPath("Salt")
   
    def test_hash(self):
        path= self.hash.path("") 
        self.assertEqual( len ( path ), self.hash.split_num )
        self.assertEqual( len ( self.hash.hash("") ), self.hash.split_num*len( path[0] ) )
        for e in path:
            self.assertEqual(len( path[0]), len(e))
        pass
'''
Created on 05.02.2013

@author: thomas
'''
from FileName import FileName
import os
import shutil

class FileTest(unittest.TestCase):

    def tearDown(self):
        shutil.rmtree('tmp') 
        pass


    def testName(self):
        f=FileName('tmp')
        f.createdirs('dir/test')
        assert(os.path.exists('tmp/dir'))
        pass
    
    def testHashFileName(self):
        name="Hi"
        hashpath=HashPath("More Salt")
        hashfile='/'.join(hashpath.path(name))

        filename=FileName('tmp')
        filename.createdirs(hashfile)
        assert(os.path.isdir(os.path.dirname('tmp/'+hashfile)))
        
        f=filename.createfile(hashfile)
        f.close()
        assert(os.path.exists(('tmp/'+hashfile)))
        
        pass

        
        
if __name__ == "__main__":
    unittest.main()