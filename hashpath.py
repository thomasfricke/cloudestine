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
                 split_num=4,
                 block_size=4096):
        self.salt = salt
        self.algorithm = algorithm
        self.split_num = split_num
        self.separator = separator
        self.block_size=block_size
        
    def hashpath(self,s):
        digest = self.algorithm(s)
        return digest.hexdigest()
    
    def path(self,name,meta='main',block=0):
        s=self.separator.join( ( self.salt, name, meta, str( block - block % self.block_size ) ) )
        splitted=HashPath.__split__(  self.hashpath(s) , self.split_num )
        return os.path.sep.join(splitted)

