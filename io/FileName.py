'''
Created on 05.02.2013

@author: thomas
'''
import os

class FileName(object):
    
    def __init__(self,base):
        self.base=base
    
    def makedirs(self,path):
        directory=os.path.dirname(self.base+"/"+path)
        if not os.path.exists(directory):
            os.makedirs(directory)
    
    def open(self,path,mode='r'):
        if mode == 'w':
            self.makedirs(path)
        return open(self.base+"/"+path, mode)