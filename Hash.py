import hashlib

class Hash(object):
    @staticmethod
    def algorithms(a):
      algos= {'md5': hashlib.md5, 
      'sha1': hashlib.sha1,
      'sha224': hashlib.sha224, 
      'sha256': hashlib.sha256,
      'sha384': hashlib.sha384, 
      'sha512': hashlib.sha512 }
      return algos[a]
      
    @staticmethod
    def __split__(arr, count):
      return [arr[i::count] for i in range(count)]
     
    def __init__(self,salt,algorithm="sha512",split_num=32):
        self.salt = salt
        self.algo = Hash.algorithms(algorithm)
        self.split_num=split_num
        
    def hash(self,s):
        digest = self.algo(self.salt + s)
        return digest.hexdigest()
    
    def path(self,s):
      return Hash.__split__(self.hash(s),self.split_num)

