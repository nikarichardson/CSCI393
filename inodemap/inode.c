#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>
#include <fcntl.h>
#include <errno.h>
#include <string.h>
#include <time.h>

#include "block_device.h"
#include "master_block.h"
#include "assert.h"
#include "dylan_bit_set.h"
#include "inode.h"

#define BLOCK_PTRS_PER_INODE_STRUCT 8                           

// STATUS 
#define STATUS_FREE 0
#define STATUS_ALLOCATED 1
#define STATUS_NEEDS_WRITING 2

// GROUP IDS 
#define OWNER 0 
#define GROUP 1
#define ALL 2 

// OCTAL PERMISSIONS 
#define NO_PERMISSION 0             // ---
#define EXECUTE_PERMISSION 1        // --x
#define WRITE_PERMISSION 2          // -w-
#define EXECUTE_N_WRITE 3           // -wx
#define READ_PERMISSION 4           // r--
#define READ_N_EXECUTE 5            // rw-
#define READ_AND_WRITE 6            // rw-
#define ALL_PERMISSIONS 7           // rwx 

// getDiskAddressOfBlock - is the main task of an iNode: map file offsets to disk
// addresses. The alloc_with_absent flag used for writes to previously unallocated blocks.
// returns a disk address of the block of data if present or if alloc_if_absent,
// or -1 otherwise

// allocate an INode and returns its address (or -1 if none free)
inode_addr_t allocateINode (INode *inode_map){
    // the argument is an array of inodes 
    int length = inode_map[0].num_inodes; 
    for (int j=0; j <= length; j = j+1){
        if (getStatus(j,inode_map) == 0){
            // sets status to STATUS_ALLOCATED
            inode_map[j].status = 1; 
            // fprintf(stdout,"inode_map[%d] has now status %d \n",j,inode_map[j].status); 
            // returns index of allocated inode 
            return inode_map[j].inode_num; 
        } 
    }
    // none are free 
    fprintf(stdout,"no free inodes in inode_map"); 
    return -1; 
}

// free an INode, i.e. marks the indicated inode as free 
// we won't free any blocks yet 
int freeINode (inode_addr_t inode_to_free,INode *inode_map){
    if (inode_map[inode_to_free].status != 0){
        // x[0] is equivalent to *x.
        inode_map[inode_to_free].status = 0; 
        return 0; 
    } else {
        //fprintf(stdout, "oops - freeing an item that is already marked free\n");
        return -1; 
    }
}

int getStatus (inode_addr_t inode,INode *inode_map){
  return inode_map[inode].status;
}

// the internal, recursive version of gDAOB, but for now only handles
// level 0 INodes
// changed blockoffset to inode_addr_t
disk_addr_t getDiskAddressOfBlockRecursive(INode_t inode, inode_addr_t b
                                          , bool alloc_if_absent, int level
                                          , BlockMap_t block_map) {
    if (level == 0) {
        if (b < BLOCK_PTRS_PER_INODE_STRUCT) {
            if (inode->block_ptrs[b] > 0) {
                return (inode->block_ptrs[b]);
            } else if (alloc_if_absent) {
                return (allocItem(block_map)); // changed from allocBlock to allocItem
            } else {
                fprintf(stderr, "block device is full!");
                return -1;
            }
        } else {
            fprintf(stderr, "we don't support INodes that big (yet)\n");
            return -1;
        }
    } else {
        fprintf(stderr, "we don't support INodes with level > 0 (yet)\n");
        return -1;
    }
}

disk_addr_t getDiskAddressOfBlock(INode_t inode, inode_addr_t b
                                    , bool alloc_if_absent, BlockMap_t bm) {
    assert(inode && inode->level >= 0);
    return getDiskAddressOfBlockRecursive(inode, b, alloc_if_absent, inode->level, bm);
}


INode *allocINodeMap(int num_inodes, int bytes_per_block){ 
    size_t n = num_inodes;
    INode *ptr = malloc(num_inodes * sizeof(INode_t)); 
    int index = 0; 
    // We allocate and initialize the INode Map array in memory, setting the status to (STATUS_FREE) 
    // (a bit flag of your choosing), the (inode_num) to the index in the array of each inode, the num_bytes to 0
    // and each of the block_ptrs array elements to 0 (which is why disk address 0 shouldn't be used for anything but the master block).
    for (size_t j = 0;  j < n;  j++)
    { 
      ptr[j].inode_num = index; 
      ptr[j].owner_uid = 501;                       // veronica's UID according to echo $UID 
      ptr[j].gid = ALL;                           
      ptr[j].type = 0; 
      ptr[j].perms = 7;                             // unallocated inodes will have all permissions rwx 
      ptr[j].status = STATUS_FREE;                  // 0 is unallocated/free, 1 is allocated, 2 is needs to be written?
      ptr[j].link_count = 0;                        // 0 hard links upon creation 
      ptr[j].cdate = time(NULL);                    // returns the time since 00:00:00 UTC, January 1, 1970 (Unix timestamp) in seconds
      ptr[j].mdate = time(NULL);                    // the most recently modified date is the creation date 
      ptr[j].level = 0;                             // for now we only use level 0 
      ptr[j].num_bytes = 0;                         // current size of the inode 
      ptr[j].num_inodes = num_inodes;               // number of inodes in the inode map 

      // initialize each of the block_ptrs array elements to 0 
      // memset takes array ptr[j].block_ptrs and initialies a BLOCK_PTRS_PER_INODE_STRUCT number of elements to 0
      memset(ptr[j].block_ptrs, 0, BLOCK_PTRS_PER_INODE_STRUCT);
      index += 1; 
    } 
    // ALLOCATE THE ROOT DIRECTORY'S INODE 
    inode_addr_t root = allocateINode(ptr); 
    fprintf(stdout, "    allocated root INode\n"); // (inode_map[%d])
    if (root == -1){
        fprintf(stderr, "    allocating INode for root directory failed\n");
    }
    return ptr; // return a pointer to an iNode map 
} 

// reads an INode map on block device bd into inode_map allocated above at disk_address
INode *readINodeMap(block_device_t bd, INode *inode_map, disk_addr_t disk_address, int num_inodes){
    // number of blocks the iNode map occupies depends on the number of iNodes we pre-allocate (num_inodes), the bytes
    // per block in the file systems (block_size) and the size of the iNode structure (sizeof(INode)) 
    int bytes_per_iNode = 32; 
    int block_size = bd->m_bytesPerBlock; 
    int ipb = ceiling(bytes_per_iNode,block_size); // inodes per block is equal to the bytes_per_inode / block_size. 
    int blocks_per_inode_map = ceiling(num_inodes,ipb); // number of inodes allocating divided by inodes per block 

    char *ret = calloc(1, blocks_per_inode_map * bd->m_bytesPerBlock);
    for (int i = 0; i < blocks_per_inode_map; i++) {
          char *buf = &ret[i * bd->m_bytesPerBlock];
          if (readBlock(bd, disk_address + i, buf) != 0) {
            fprintf(stderr, "error reading inode map\n");
            return NULL;
          }
      }

    // check the pointer work here!!! 
    INode *rbs = (INode *)ret; // rbs[0].status == 0
    if (rbs[0].status == 0) {
      fprintf(stderr, "something went wrong while reading INode map — root is not allocated \n");
      return NULL; 
    }
    return rbs; 
}

// writes an INode map to block device bd from inode_map at disk_address 
int writeINodeMap(block_device_t bd, INode *inode_map, disk_addr_t disk_address, int num_inodes){
    int bytes_per_iNode = 32; 
    int block_size = bd->m_bytesPerBlock; 
    int ipb = ceiling(bytes_per_iNode,block_size); // inodes per block is equal to the bytes_per_inode / block_size. 
    int blocks_per_inode_map = ceiling(num_inodes,ipb); // number of inodes allocating divided by inodes per block 
    
    char *buf = (char *)inode_map;
    for (int i = 0; i < blocks_per_inode_map; i++) {
        char *bbuf = &buf[i * bd->m_bytesPerBlock];
        if (writeBlock(bd, disk_address + i, bbuf) != 0) {
            fprintf(stderr, "error writing inode map\n");
            return -1;
        }
    }
    return 0;
}


