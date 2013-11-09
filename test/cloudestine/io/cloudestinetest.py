#!/usr/bin/env python 

import unittest2
from cloudestine.cloudestine import Cloudestine
from signal import SIGKILL
from time import sleep
import sys


'''
Created on 05.02.2013

@author: thomas
'''
import os
import shutil



class CloudestineTest(unittest2.TestCase):
    def unmount(self):
        os.system("fusermount -u %s" % self.fusedir)

    def __init__(self,test_name):
        super(CloudestineTest, self).__init__(test_name)
        self.basedir='/tmp/cloudestine'
        self.fusedir=self.basedir+'/mount'
        self.storage_dir=self.basedir+'/storage' 
              
    def tearDown(self):
        if self.is_mounted() >0:
            self.unmount()
            if self.child >0 :
                os.kill(self.child, SIGKILL )
        if os.path.isdir(self.basedir):
            shutil.rmtree(self.basedir) 
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
            working_directory = self.fusedir
            
            if mount_point != working_directory:
                continue
            
            if fuse != 'fuse':
                continue
           
            if mount_point != self.fusedir :
                continue
          
            print line
            print array

            found = True
            break
        
        proc_mount.close()
        
        return found
    
    def test_Cloudestine_file_system_start_and_stop(self):
        Cloudestine(True,self.fusedir,None)
        
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
     
    def test_Cloudestine_write_read_file(self):
        cloudestine = Cloudestine(True,self.fusedir,None) 
        cloudestine.create("file", 0x644)
        
        
if __name__ == "__main__":
    unittest2.main()