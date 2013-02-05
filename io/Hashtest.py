#!/usr/bin/env python 

import unittest
from io.HashPath import HashPath

class Hashtest(unittest.TestCase):

    def setUp(self):
        self.hash = HashPath("Salt")

   
    def test_hash(self):
        path= self.hash.path("") 
        self.assertEqual( len ( path ), self.hash.split_num )
        self.assertEqual( len ( self.hash.hash("") ), self.hash.split_num*len( path[0] ) )
        for e in path:
            self.assertEqual(len( path[0]), len(e))
        pass

if __name__ == '__main__':
    unittest.main()
