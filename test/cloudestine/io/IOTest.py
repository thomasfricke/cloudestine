#!/usr/bin/env python 

import unittest
from  cloudestine.io.hashpath import HashPath
from cloudestine.cloudestine import Cloudestine
from signal import SIGTERM, SIGKILL
from time import sleep
import sys

class Hashtest(unittest.TestCase):

    def setUp(self):
        self.hash = HashPath("Salt")
   
    def test_hashpath_and_count_parts(self):
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
from cloudestine.io.filename import FileName
import os
import shutil
from cloudestine.fuse import FUSE

class CloudestineTest(unittest.TestCase):
    
    def tearDown(self):
        if self.count_Cloudestine() >0:
            os.system("sudo umount tmp")
            if self.child >0 :
                os.kill(self.child, SIGKILL )
        
        if os.path.isdir('tmp'):
            shutil.rmtree('tmp') 
        pass
    
    def setUp(self):
        self.child=-1
        os.makedirs('tmp')
        pass
    
    def count_Cloudestine(self):
        found=0
        
        proc_mount=file('/proc/mounts','r')
        for mount_point in proc_mount.readlines():
            if mount_point.startswith("Cloudestine"):
                found += 1
        proc_mount.close()
        
        return found
    
    def test_Cloudestine_file_system_start(self):
        cloudestine = Cloudestine(True,"tmp")
        
        self.assertEqual(self.count_Cloudestine(),0, "should not run" )
   
        self.child=os.fork()
        
        if self.child == 0 :
            fuse = FUSE( cloudestine,"tmp", foreground=False )
            sys.exit(0)
            
        sleep(2)
        self.assertEqual(self.count_Cloudestine(),1, "should run" )
        
        os.system("sudo umount tmp")
       
        
        self.assertEqual(self.count_Cloudestine(),0, "should not run" )
        
        
        
        
class FileTest(unittest.TestCase):

    def tearDown(self):
        shutil.rmtree('tmp') 
        pass


    def testName(self):
        f=FileName('tmp')
        f.makedirs('dir/test')
        assert(os.path.exists('tmp/dir'))
        pass
    
    def test_makedirs_with_HashFileName_and_create_write_and_read_file(self):
        name="Hi"
        hashpath=HashPath("More Salt")
        hashfile='/'.join(hashpath.path(name))

        filename=FileName('tmp')
        filename.makedirs(hashfile)
        assert(os.path.isdir(os.path.dirname('tmp/'+hashfile)))
        
        f=filename.open(hashfile,'w')
        f.write("fine!")
        f.close()
        assert(os.path.exists(('tmp/'+hashfile)))
        
        f=filename.open(hashfile,'r')
        line=f.readline()
        f.close()

        assert( line == "fine!")
        pass

        
        
if __name__ == "__main__":
    unittest.main()