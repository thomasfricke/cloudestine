Cloudestine
===========
Cloud ready fuse filesystem with strong cryptographic capabilities

Design goals:

- not private data is unencrypted in the storage directory
- every file will be encrypted by a different symmetric key
- symmetric keys are exchanged using public key encryption
- ownership of a file is taken by the files key
- ownership is shared by sharing the files key

