import unittest2

from hashpath import HashPath
import hashlib
import string
class HashTestSha1(unittest2.TestCase):

    def __init__(self,test_name):
        super(HashTestSha1, self).__init__(test_name)
        
    def setUp(self):
        self.hashpath = HashPath("Salt",separator="\n")
        self.hash_of_Test = hashlib.sha1('Salt\nTest\nmain\n0').hexdigest()
        
    def test_hashpath_split(self):
        
        self.assertEqual(self.hash_of_Test,''.join(HashPath.__split__(self.hash_of_Test, self.hashpath.split_num)))
        
    def test_hashpath_and_count_parts(self):
        path= self.hashpath.path('Test',"main")
        self.assertEqual(len(path), len(self.hash_of_Test)+9)
        self.assertEqual(self.hash_of_Test, string.replace(path, '/', '', 9))
        
        
class HashTestMd5(unittest2.TestCase):

    def __init__(self,test_name):
        super(HashTestMd5, self).__init__(test_name)
        
    def setUp(self):
        self.hashpath = HashPath("Salt",separator="#", algorithm=hashlib.md5)
        self.hash_of_Test = hashlib.md5('Salt#Test#main#0').hexdigest()
        
    def test_hashpath_split(self):
        
        self.assertEqual(self.hash_of_Test,''.join(HashPath.__split__(self.hash_of_Test, self.hashpath.split_num)))
        
    def test_hashpath_and_count_parts(self):
        path= self.hashpath.path('Test',"main")
        self.assertEqual(len(path), len(self.hash_of_Test)+7)
        self.assertEqual(self.hash_of_Test, string.replace(path, '/', '', 7))

if __name__ == '__main__':
    unittest2.main()