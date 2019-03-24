INode + INodeMap Assignment 
By Nika R. 

Beginning with Dylan's implementation of assignment 2, including the Master Block and the BlockMap. 

To run, decompress the file as necessary and type make into the terminal once you are inside the right directory. 

I have two test runs for the blockmap code—primarily, holdovers from the last project (mytestFs.py and testFSsmall.py)— and two test runs for iNode map: inodetest.py and inodetestsmall.py 

I implement the following functions: 

	// allocate an INode and returns its address (or -1 if none free)
	inode_addr_t allocateINode (INode* inode_map); 

	// free an INode
	int freeINode (inode_addr_t inode_to_free,INode* inode_map);

	// allocate INode map 
	INode *allocINodeMap(int num_inodes, int bytes_per_block); 

	// ceiling function for computations
	int ceiling(int x, int y); 

	// getStatus function; returns the status number of INode in question
	int getStatus (inode_addr_t inode,INode *inode_map); 

	// read INod eMap from block device into the pre-allocated inode map. 
	INode *readINodeMap(block_device_t bd, INode* inode_map, disk_addr_t disk_address, int num_inodes);

	// write an INode Map to block device
	int writeINodeMap(block_device_t bd, INode* inode_map, disk_addr_t disk_address, int num_inodes);

A few bugs I had: First, I was testing the blockmap tests to make sure that the blockmap and masterblock functions would still run normally after adding iNode code. I noticed that the changes I was making to the blockmap were seemingly not being written to disk, since after unmounting and remounting, the changes were not preserved. As it turns out, I had changed the device name in the top part of myTest.py and not in the second half, so I was making changes to one device and then mounting another device (!!). Once I fixed it, the changes made to my blockmap were effectively written to disk. 

My second brilliant error from Sunday night: my readINodeMap seemed to be working, but I noticed that the root directory was never allocated. After some time, I finally realized that I had forgotten to write the INodeMap to disk in my newfs function (filesystem.c)

For better or for worse, the two errors are above are the greatest problems I encountered while working on this assignment. Alas, they were pretty frustrating at the time because I had no idea what was going haywire! My brain, apparently. 

Addendum: So it's Wednesday evening-ish when I realize that I never tested that my inode map is preserved throughout the mounting and unmounting process. I too am surprised by this testing omission. In fact, my iNode map was not being preserved, because I neglected to modify the unmount in my_shell.c. That issue is now resolved. All should be well now. 
