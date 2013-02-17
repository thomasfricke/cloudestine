#!/usr/bin/env python 

import unittest
from  cloudestine.io.hashpath import HashPath
from cloudestine.cloudestine import Cloudestine
from signal import SIGKILL
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
    def unmount(self):
        os.system("fusermount -u %s" % self.fusedir)

    def __init__(self,test_name):
        super(CloudestineTest, self).__init__(test_name)
        self.fusedir='cloudestine/mount'
        self.storage_dir='cloudestine/storage' 
              
    def tearDown(self):
        if self.is_mounted() >0:
            self.unmount()
            if self.child >0 :
                os.kill(self.child, SIGKILL )
        for d in (self.fusedir,self.storage_dir):
            if os.path.isdir(d):
                shutil.rmtree(d) 
                pass
    
    def setUp(self):
        self.child=-1
        os.makedirs(self.fusedir)
        pass
    
    def is_mounted(self):
        found=False
        
        proc_mount=file('/proc/mounts','r')
        for line in proc_mount.readlines():
            
            array=line.split(' ')

            if len(array)<3:
                continue 
            (fs, mount_point, fuse)=array[0:3]
            if fs != 'Cloudestine':
                continue
            working_directory = os.getcwd()+"/"+self.fusedir
            if mount_point != working_directory:
                continue
            if fuse != fuse:
                continue
          
            print line
            print array

            found = True
            break
        
        proc_mount.close()
        
        return found
    
    def test_Cloudestine_file_system_start(self):
        cloudestine = Cloudestine(True,self.fusedir,None)
        
        self.assertFalse(self.is_mounted(), "should not run" )
   
        self.child=os.fork()
        
        if self.child == 0 :
            Cloudestine.main([self.fusedir,None])
            sys.exit(0)
            
        sleep(2)
        self.assertTrue(self.is_mounted(), "should run" )
        
        self.unmount()       
        sleep(2)
        
        self.assertFalse(self.is_mounted(), "should not run" )
        
        
        
        
class FileTest(unittest.TestCase):

    def __init__(self,test_name):
        super(FileTest, self).__init__(test_name)
        self.tmpdir = 'tmp'
   
    def tearDown(self):
        shutil.rmtree(self.tmpdir) 
        pass


    def testName(self):
        f=FileName(self.tmpdir)
        f.makedirs('dir/test')
        assert(os.path.exists('tmp/dir'))
        pass
    
    def test_makedirs_with_HashFileName_and_create_write_and_read_file(self):
        name="Hi"
        hashpath=HashPath("More Salt")
        hashfile='/'.join(hashpath.path(name))

        filename=FileName(self.tmpdir)
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