'''
Created on 05.02.2013

@author: thomas
'''
import os

class FileName(object):
    
    def __init__(self,base,path):
        self.base = base
        self.path = path
        self.directory = base + os.sep + os.path.dirname(path)
        self.filename  = base + os.sep + path
    
    def makedirs(self):
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)
    
    def open(self,mode='r'):
        if mode == 'w':
            self.makedirs()
        return open(self.filename, mode)