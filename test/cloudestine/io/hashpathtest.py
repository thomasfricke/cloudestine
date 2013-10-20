import unittest2

from cloudestine.io.hashpath import HashPath
import hashlib

class HashTest(unittest2.TestCase):

    def __init__(self,test_name):
        super(HashTest, self).__init__(test_name)
        
    def setUp(self):
        self.hash = HashPath("Salt")
        self.hash_of_Test = hashlib.sha1('SaltTest').hexdigest()
        
    def test_hashpath_split(self):
        
        self.assertEqual(self.hash_of_Test,''.join(HashPath.__split__(self.hash_of_Test, self.hash.split_num)))
        
    def test_hashpath_and_count_parts(self):
        path= self.hash.path('Test')
        self.assertEqual(self.hash_of_Test, ''.join(path))
        self.assertEqual(hashlib.sha1('SaltTest').hexdigest(),''.join(path))
        self.assertEqual( len ( path ), len(self.hash_of_Test) / self.hash.split_num )
        self.assertEqual( len (self.hash_of_Test ), self.hash.split_num*len( path) )
        for e in path:
            self.assertEqual(len( path[0]), len(e))
        pass