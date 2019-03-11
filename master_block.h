#ifndef MASTERBLOCK_H
#define MASTERBLOCK_H
#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>
#include <fcntl.h>
#include <errno.h>
#include <stdbool.h>
#include <string.h>
#include <assert.h>
#include "block_device.h"


// =================================================
// Master Block 
// =================================================
typedef struct MasterBlock {
	uint64_t magic_num; // 
	uint32_t bytes_per_block; // must match that of the Block Device  BLOCK_SIZE 
	disk_addr_t blocks_per_device; // number of blocks = BLOCKS_PER_DEVICE = BlockCount  
	disk_addr_t disk_addr_of_block_map; // number of blocks  between start of disk and block in question
} MasterBlock, *master_block_t;

master_block_t allocMasterBlock (int bytes_per_block, int number_of_blocks, disk_addr_t block_map_address);

int readMasterBlock(BlockDevice *bd, MasterBlock *mb, disk_addr_t disk_location); // only need to do once @ mount

int writeMasterBlock(BlockDevice *bd, MasterBlock *mb, disk_addr_t disk_location); // newfs and unmount done twice 

void freeMasterBlock(master_block_t mb);

int bootstrapDeviceFromMasterBlock(BlockDevice *bd);

#endif /* MASTERBLOCK_H */ 