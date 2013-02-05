'''
Created on 05.02.2013

@author: thomas
'''
import os

class File(object):
    
    def __init__(self,base):
        self.base=base
    
    def create(self,path):
        os.makedirs(self.base+"/"+path)