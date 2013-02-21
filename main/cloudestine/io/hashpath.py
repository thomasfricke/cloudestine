'''
class to map filenames and paths to hashes
@author: thomas
'''
import hashlib
class HashPath(object):
    algos= {'md5': hashlib.md5, 
            'sha1': hashlib.sha1,
            'sha224': hashlib.sha224, 
            'sha256': hashlib.sha256,
            'sha384': hashlib.sha384, 
            'sha512': hashlib.sha512 }
    
      
    @staticmethod
    def __split__(arr, count):
        return [arr[i::count] for i in range(count)]
     
    def __init__(self,salt,algorithm="sha1",split_num=4):
        self.salt = salt
        self.algo = HashPath.algos[algorithm]
        self.split_num=split_num
        
    def hash(self,s):
        digest = self.algo(self.salt + s)
        return digest.hexdigest()
    
    def path(self,s):
        return HashPath.__split__(self.hash(s),self.split_num)

