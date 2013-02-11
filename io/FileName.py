'''
Created on 05.02.2013

@author: thomas
'''
import os

class FileName(object):
    
    def __init__(self,base):
        self.base=base
    
    def createdirs(self,path):
        directory=os.path.dirname(self.base+"/"+path)
        if not os.path.exists(directory):
            os.makedirs(directory)
    
    def createfile(self,path):
        self.createdirs(path)
        return open(self.base+"/"+path, "w")