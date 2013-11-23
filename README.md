Cloudestine
===========
Cloud ready fuse filesystem with strong cryptographic capabilities

Design goals:

- no private data is unencrypted in the storage directory
- every file will be encrypted by a different symmetric key
- symmetric keys are exchanged using public key encryption
- ownership of a file is taken by the files key
- ownership is shared by sharing the files key
- trust operations are mapped to file operations

Howto test:

1. You need a working fuse.py in some directory FUSEPY.

This is the directory where you checked out 

   git clone  https://github.com/terencehonles/fusepy.git

   FUSEPY=$(PWD)/fusepy
   
Set the Python path to the cloudestine directory where you 
have checked out and the FUSEPY directory.

2. Download the sources with

   git clone https://github.com/thomasfricke/cloudestine.git
   
3. For simplicity we do everything in the cloudestine directory

   cd cloudestine
   export PYTHONPATH=$(PWD)/main:$FUSEPY
   
4. Run the tests

   python -m unittest2 discover  -s main

5. Credits: 

Thanks to Matthias Schmitz for forcing me to make it work outside of Eclipse.
