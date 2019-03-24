#pragma once

#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>
#include <fcntl.h>
#include <errno.h>
#include <string.h>
#include <time.h>

#include "block_device.h"
#include "master_block.h"
#define BLOCK_PTRS_PER_INODE_STRUCT 8 							// can be any length; we choose 8

typedef int inode_addr_t;
typedef int inode_type_t; 

typedef struct INode {
	inode_addr_t 	inode_num; 									// which inode this is (index in the inode map)
	uint32_t		owner_uid;  								// who owns this
	uint32_t 		gid;  										// which group id the perms refer to
	inode_type_t	type;   									// file, directory, symlink, ...
	uint16_t 		perms; 										// RWX permissions for owner / group / all
	uint16_t 		status; 									// whether it's allocated, needs to be written, etc
	uint16_t		link_count; 								// how many hard links there are to this INode 
	time_t			cdate;   									// creation_time
	time_t			mdate; 										// most recent modification time
	uint16_t		level; 										// level
	uint64_t  		num_bytes; 									// the current size of the inode
	disk_addr_t	block_ptrs[BLOCK_PTRS_PER_INODE_STRUCT]; 	    // data blocks, or blocks of disk_address_t[]
	int 			num_inodes;									// number of inodes in the map
} INode, *INode_t; 

// allocate an INode and returns its address (or -1 if none free)
inode_addr_t allocateINode (INode* inode_map); 

// free an INode
int freeINode (inode_addr_t inode_to_free,INode* inode_map);

typedef int inode_addr_t;
typedef int inode_type_t; 

INode *allocINodeMap(int num_inodes, int bytes_per_block); 

int ceiling(int x, int y); 

int getStatus (inode_addr_t inode,INode *inode_map); 

INode *readINodeMap(block_device_t bd, INode* inode_map, disk_addr_t disk_address, int num_inodes);

int writeINodeMap(block_device_t bd, INode* inode_map, disk_addr_t disk_address, int num_inodes);


