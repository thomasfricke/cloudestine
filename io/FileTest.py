'''
Created on 05.02.2013

@author: thomas
'''
import unittest
from File import File
import os
import shutil
from io.HashPath import HashPath

class FileTest(unittest.TestCase):

    def tearDown(self):
        shutil.rmtree('tmp') 
        pass


    def testName(self):
        f=File('tmp')
        f.create('test')
        assert(os.path.exists('tmp/test'))
        pass
    
    def testHashFileName(self):
        name="Hi"
        hashpath=HashPath("More Salt")
        hash='/'.join(hashpath.path(name))
        print hash
        f=File('tmp')
        f.create(hash)
        assert(os.path.exists('tmp/'+hash))
        pass

        
        
if __name__ == "__main__":
    unittest.main()