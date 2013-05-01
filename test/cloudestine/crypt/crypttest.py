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
           
        cpuMHz=-1

        with open("/proc/cpuinfo","r") as f:
            for line in f:
                if line.startswith("cpu MHz"):
                    cpuMHz=float(line.split(":")[1])
                    f.close()
                    break
            

        created_keys=[]
        i=0
        while i<10:
            start=time.time()
            created_keys.append( crypt.create("test@example.com", "passphrase",
                                              key_length=256).__str__() )
            i+=1
            stop=time.time()
            print "start=%f stop=%f" %(start,stop)
            self.assertLess(cpuMHz *(stop-start), 20000.0, 
                            "system is to slow, check entropy gathering")
        
        ascii_armored_public_keys = crypt.gpg.export_keys(created_keys)
        self.assertTrue(ascii_armored_public_keys.
                        startswith("-----BEGIN PGP PUBLIC KEY BLOCK-----"),
                        "no public created_keys" + ascii_armored_public_keys)
        self.assertTrue(ascii_armored_public_keys.
                        endswith("-----END PGP PUBLIC KEY BLOCK-----\n"),
                        "no public created_keys: " + ascii_armored_public_keys )
        ascii_armored_private_keys = crypt.gpg.export_keys(created_keys, True)
        self.assertTrue(ascii_armored_private_keys.
                        startswith("-----BEGIN PGP PRIVATE KEY BLOCK-----"),
                        "no public created_keys" + ascii_armored_private_keys)
        self.assertTrue(ascii_armored_private_keys.
                        endswith("-----END PGP PRIVATE KEY BLOCK-----\n"),
                        "no public created_keys: " + ascii_armored_private_keys )
        
        found_key=0
        for created_key in created_keys:
            for key in crypt.list_keys():
                if key['fingerprint'] == created_key:          
                    found_key+=1
        
        self.assertEqual(found_key ,len( created_keys) , "where are my keys")
        pass
    
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest2.main()