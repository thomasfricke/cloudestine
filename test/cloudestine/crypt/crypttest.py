'''
Created on 23.02.2013

@author: thomas
'''
import unittest2
import shutil
import time
import os

from cloudestine.crypt.gpg import Crypt

class CryptTest(unittest2.TestCase):
    
    def __init__(self,test_name):
        super(CryptTest, self).__init__(test_name)
        self.basedir='/tmp/cloudestine'
        
    def tearDown(self):
        if os.path.isdir(self.basedir):
            shutil.rmtree(self.basedir) 
        pass
    
    def setUp(self):
        print "create ",self.basedir
        os.makedirs(self.basedir)
        self.assertTrue(os.path.isdir(self.basedir), "where is my dir")
        pass

    def test_gpg(self):
        crypt=Crypt(self.basedir)
        
        f=open("/proc/cpuinfo","r")
        cpuMHz=-1
        for line in f:
            if line.startswith("cpu MHz"):
                cpuMHz=float(line.split(":")[1])
                break
            
        f.close

        start=time.clock()
        crypt.create("test@example.com", "passphrase")
        stop=time.clock()
        print "start=%f stop=%f" %(start,stop)
        self.assertLess(cpuMHz *(stop-start), 48.0, "system is to slow, check entropy gathering")
        pass
    
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest2.main()