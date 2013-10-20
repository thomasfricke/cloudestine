'''
class to map filenames and paths to hashes
@author: thomas
'''
import hashlib
class HashPath(object):
          
    @staticmethod
    def __split__(arr, count):
        return [arr[i:i+count] for i in range(0, len(arr), count)]
     
    def __init__(self,salt,algorithm=hashlib.sha1,split_num=4):
        self.salt = salt
        self.algorithm = algorithm
        self.split_num=split_num
        
    def hash(self,s):
        digest = self.algorithm(self.salt + s)
        return digest.hexdigest()
    
    def path(self,s):
        return HashPath.__split__(self.hash(s),self.split_num)

