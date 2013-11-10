'''
class to map filenames and paths to hashes
@author: thomas
'''
import hashlib
import os
class HashPath(object):
          

    @staticmethod
    def __split__(arr, count):
        return [arr[i:i+count] for i in range(0, len(arr), count)]
     
    def __init__(self,salt,
                 separator='\n',
                 algorithm=hashlib.sha1,
                 split_num=4):
        self.salt = salt
        self.algorithm = algorithm
        self.split_num = split_num
        self.separator = separator
        
    def hashpath(self,s):
        digest = self.algorithm(s)
        return digest.hexdigest()
    
    def path(self,name,meta='main',block=0):
        s=self.separator.join( ( self.salt, name, meta, str(block)  ) )   
        return os.sep.join(HashPath.__split__( self.hashpath(s), self.split_num ))

