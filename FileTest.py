'''
Created on 05.02.2013

@author: thomas
'''
import unittest
from File import File
import os
import shutil

class FileTest(unittest.TestCase):

    def tearDown(self):
        shutil.rmtree('tmp') 
        pass


    def testName(self):
        f=File('tmp')
        f.create('test')
        assert(os.path.exists('tmp/test'))
        pass


if __name__ == "__main__":
    unittest.main()