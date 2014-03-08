#!/usr/bin/env python 

import unittest2
from cloudestine import Cloudestine
from signal import SIGKILL
from time import sleep
import logging
from dirspec import basedir

logging.basicConfig()
log=logging.getLogger(__name__)

'''
Created on 05.02.2013

@author: thomas
'''
import os
import shutil

basedir='/tmp/cloudestine'

class CloudestineTest(unittest2.TestCase):
    
    fuse_dir=basedir+'/mount'
    storage_dir=basedir+'/base_name' 
    child=-1
    
    @classmethod
    def mount_cloudestine(cls, wait=10):
        Cloudestine(True, 
                    mount   = cls.fuse_dir,
                    base_name =cls.storage_dir)
        
        CloudestineTest.child=child=os.fork()
        
        if child == 0 :
            Cloudestine.main([cls.fuse_dir, cls.storage_dir])
            return
        
        CloudestineTest.wait_for_mount_unmount("mount", wait)
      
    @classmethod    
    def unmount_cloudestine(wait=10):
        os.system("fusermount -u %s" % CloudestineTest.fuse_dir)
        CloudestineTest.wait_for_mount_unmount("unmount", wait)
    
    @classmethod    
    def wait_for_mount_unmount(cls,mount, wait):
        count=0
        while  ( ( CloudestineTest.is_mounted() == ( mount=="unmount" ) ) 
                 and  ( count < wait ) ):
            sleep(1)
            count+=1
            log.debug("waiting for %s: %d/%d" %(mount,count,wait) )
        
        if(count==wait):
            msg="mount of dir %s failed" % CloudestineTest.fuse_dir
            log.error(msg)
            raise Exception(msg)
        log.debug("filesystem "+ mount+"ed")
        
    def __init__(self,test_name):
        super(CloudestineTest, self).__init__(test_name)
             
    def tearDown(self):
        log.debug("start tearDown")
       
        pass
    
    @classmethod
    def setUpClass(cls):
        super(CloudestineTest, cls).setUpClass()
        
        if os.path.isdir(basedir):
            shutil.rmtree(basedir,ignore_errors=True)
        
        os.makedirs(CloudestineTest.fuse_dir)
        os.makedirs(CloudestineTest.storage_dir)
        assert(os.path.isdir(CloudestineTest.fuse_dir))
        cls.mount_cloudestine()
    
    @classmethod
    def list_cloudestinedir_recursively(clazz):
        for dirname, dirnames, filenames in os.walk(basedir):
        # print path to all subdirectories first.
            for subdirname in dirnames:
                log.debug( os.path.join(dirname, subdirname) )
        
            # print path to all filenames.
            for filename in filenames:
                log.debug(  os.path.join(dirname, filename) )
        
            # Advanced usage:
            # editing the 'dirnames' list will stop os.walk() from recursing into there.
            if '.git' in dirnames:
                # don't go into any .git directories.
                dirnames.remove('.git')
                    
    @classmethod
    def tearDownClass(cls):
        CloudestineTest.list_cloudestinedir_recursively()
        CloudestineTest.unmount_cloudestine()       
        
        if CloudestineTest.is_mounted() >0:
            CloudestineTest.unmount_cloudestine()
            if CloudestineTest.child >0 :
                os.kill(CloudestineTest.child, SIGKILL )
        if os.path.isdir(CloudestineTest.basedir):
            shutil.rmtree(CloudestineTest.basedir) 
        
        for directory in [CloudestineTest.fuse_dir, CloudestineTest.storage_dir]:
            if os.path.isdir(directory):
                os.rmdir(directory)
        
        if os.path.isdir(basedir):
            shutil.rmtree(basedir,ignore_errors=True)
        
        log.debug("stop tearDown")
        
        super(CloudestineTest,cls).tearDownClass()
           
    @classmethod
    def is_mounted(cls):
        found=False
        
        proc_mount=file('/proc/mounts','r')
        for line in proc_mount.readlines():
            
            array=line.split(' ')

            if len(array)<3:
                continue 
            (fs, mount_point, fuse)=array[0:3]
            if fs != 'Cloudestine':
                continue
            working_directory = cls.fuse_dir
            
            if mount_point != working_directory:
                continue
            
            if fuse != 'fuse':
                continue
           
            if mount_point != cls.fuse_dir :
                continue
          
            log.debug("line=%s" % line)
            log.debug("array=%s" % array.__str__())

            found = True
            break
        
        proc_mount.close()
        
        return found
    
    def test_Cloudestine_is_mounted(self):
        log.debug("create_file")
        self.assertTrue(CloudestineTest.is_mounted(), "should run" )
               
        
    def test_Cloudestine_write_read_file(self):
        
        self.assertTrue(CloudestineTest.is_mounted(), "should run" )
        self.assertTrue(os.path.isdir(CloudestineTest.fuse_dir))
        
        filename=CloudestineTest.fuse_dir+os.path.sep+ "file"
        log.debug("opening " + filename)
        f=open(filename, "a")
        log.debug("open")
        
        self.assertTrue(CloudestineTest.is_mounted(),"should run")
        self.assertTrue(os.path.exists(filename))
        content="fine!"
        f.write(content)
        f.close()
        log.debug(f)
      
        
if __name__ == "__main__":
    unittest2.main()