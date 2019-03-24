#include "filesystem.h"
#include "block_device.h"
#include "master_block.h"
#include "dylan_bit_set.h"
#include "inode.h"
#include "assert.h"

int ceiling(int x, int y) {
    return x / y + (x % y > 0);
}

int newfs(char *device_filename, int block_size, int block_count) {
    assert(device_filename && "NULL filename to newfs");
    BlockDevice *bd = createBlockDevice(device_filename, block_size, block_count);
    if (bd == NULL) return -1;
    if (block_size < sizeof(MasterBlock)) {
        fprintf(stderr, "block size needs to be >= sizeof(MasterBlock) (%d)\n", (int)sizeof(MasterBlock));
        return -1;
    }
    // allocate a fresh Master Block structure
    int block_map_location = 1;
    master_block_t mb = allocMasterBlock(block_size, block_count, block_map_location);
    assert (mb && "allocMasterBlock failed");
    BlockMap_t bs = allocBlockMap(block_count, block_size);
    assert(bs && "allocBlockMap failed");
    // mark the first X blocks as allocated
    int blocks_in_blockmap = getBlocksInBlockMap(bd);
    int prealloc_blocks = blocks_in_blockmap + 1; // count the master block!
    if (block_count <= prealloc_blocks) {
        fprintf(stderr, "block count needs to be at least Master Block + block map blocks (%d)\n", prealloc_blocks);
        return -1;
    }
    // printf("\n prealloc blocks is %d \n",prealloc_blocks); ONLY 2 PREALLOCATED BLOCKS IN OUR EXAMPLE 
    for (int i = 0; i < prealloc_blocks; i++) {
        assert(allocItem(bs) >= 0 && "device too small for preallocated blocks!"); // shouldn't happen - check above
    }

    // Add disk_address_of_inode_map to the Master Block, and initialize it to the block after the Block Map
    mb->inode_map_address = prealloc_blocks+1;

    // write the master block to the device @ disk address 0
    if (0 > writeMasterBlock(bd, mb, 0)) {
        fprintf(stderr, "write master block failed\n");
        return -1;
    }
    
    int num_inodes = 100;                                        		
    INode *inodemap = allocINodeMap(num_inodes,block_size);
    assert (inodemap && "allociNodeMap failed");
    assert (inodemap[0].status == 1 && "allocating root iNode failed");

    // Write the INode Map array to disk, starting at disk address master_block->disk_address_of_inode_map.
    if (0 > writeINodeMap(bd, inodemap, mb->inode_map_address,num_inodes)){
        fprintf(stderr, "write INode map failed\n");
        return -1;
    }
    // The number of blocks depends on the number of INodes we pre-allocate (num_inodes), the bytes_per_block (block_size)
    // and the size of the INODE structure. 
    // check to make sure our block_size, or bytes_per_block, is a multiple of the bytes per iNode
    int bytes_per_iNode = 32;                                           // How many bytes per inode? 

    // in block size of 1024 this will pack 32 inodes into 1 block 
    int ipb = ceiling(block_size,bytes_per_iNode);                      // inodes per block is equal to the bytes_per_inode / block_size. 
    // should be 1024/32 in our main example

    // printf("\n ipb is %d should be 32",ipb); // ipb is right!!!
    int blocks_for_inode_map = ceiling(num_inodes,ipb);                 // number of inodes allocating divided by inodes per block 
    // blocks for inode map should be 4? 4 blocks allocated is correct for our given numbers
    if (block_size % bytes_per_iNode  != 0){
        printf("bytes_per_block must be a multiple of %d bytes",bytes_per_iNode); 
        return -1;
    }
    // Mark the associated blocks in the Block Map as being allocated.
    for (int c = 0; c < blocks_for_inode_map; c += 1){
         allocItem(bs);  
    } // correct number of allocated blocks for inode map 
    

    // we need to write the inode map to the block device u dummy!! 
    if (0 > writeINodeMap(bd,inodemap,prealloc_blocks,num_inodes)) {
        fprintf(stderr, "write iNode map failed\n");
        return -1;
    }

    // write the block map to the device starting @ disk address 1
    if (0 > writeBlockMap(bd, bs, 1)) {
        fprintf(stderr, "write block map failed\n");
        return -1;
    }
    closeBlockDevice(bd);
    free(mb);
    free(bs);
    return 0; 
}
