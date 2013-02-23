import os
import shutil
import unittest2

from filename import FileName
from hashpath import HashPath

class FileTest(unittest2.TestCase):

    def __init__(self,test_name):
        super(FileTest, self).__init__(test_name)
        self.tmpdir = 'tmp'
   
    def setUp(self):
        pass
   
    def tearDown(self):
        shutil.rmtree(self.tmpdir) 
        pass


    def test_name(self):
        pass
        f=FileName(self.tmpdir)
        f.makedirs('dir/test')
        assert(os.path.exists('tmp/dir'))
        pass
    
    def test_makedirs_with_HashFileName_and_create_write_and_read_file(self):
        pass
        name="Hi"
        hashpath=HashPath("More Salt")
        hashfile='/'.join(hashpath.path(name))

        filename=FileName(self.tmpdir)
        filename.makedirs(hashfile)
        assert(os.path.isdir(os.path.dirname('tmp/'+hashfile)))
        
        f=filename.open(hashfile,'w')
        f.write("fine!")
        f.close()
        assert(os.path.exists(('tmp/'+hashfile)))
        
        f=filename.open(hashfile,'r')
        line=f.readline()
        f.close()

        assert( line == "fine!")
        pass
    
if __name__ == "__main__":
    unittest2.main()