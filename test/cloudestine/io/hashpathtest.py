import unittest2

from cloudestine.io.hashpath import HashPath

class Hashtest(unittest2.TestCase):

    def setUp(self):
        self.hash = HashPath("Salt")
   
    def test_hashpath_and_count_parts(self):
        path= self.hash.path("") 
        self.assertEqual( len ( path ), self.hash.split_num )
        self.assertEqual( len ( self.hash.hash("") ), self.hash.split_num*len( path[0] ) )
        for e in path:
            self.assertEqual(len( path[0]), len(e))
        pass