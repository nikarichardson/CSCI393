// VR
// Block Map

#include "block_device.h"
#include "master_block.h"
#include "block_map.h"

#include <stdlib.h>
#include <unistd.h>
#include <errno.h>
#include <string.h>
#include <assert.h>
#include <stdbool.h>
#define MAGIC 0xFEEDC0DE
#define BLOCKSIZE 1024
#define BLOCKS_PER_DEVICE 100

// =============== =============== BLOCK MAP A P I =============== =============== 
// =============== =============== BlockMap (Allocate) =============== =============== 
BlockMap* allocBlockMap(int num_bits) {
	// BlockMap_p ret = calloc(1, sizeof(BlockMap));
	BlockMap_p ret = calloc(1, sizeof(BLOCKSIZE));
	ret->buffer = calloc(num_bits, sizeof(char));
	ret->count = num_bits;
	setBit(ret, 0); 
	setBit(ret, 1); 
	return ret;
}

// =============== =============== BlockMap (Free) =============== =============== 
// frees a BlockMap
void freeBlockMap(BlockMap* bs) {
	free(bs->buffer);
	free(bs);
}

// sets bit i of the BlockMap
void setBit(BlockMap* b, int i) {
	SET_BIT(b->buffer, i);
}

// clears bit i of the BlockMap
void clearBit(BlockMap* b, int i) {
	CLEAR_BIT(b->buffer, i);
}

// returns the bit (boolean) value of the ith bit/block of the BlockMap
bool getBit(BlockMap* b, int i) {
	return GET_BIT(b->buffer, i);
}

// =============== =============== BlockMap (Alloc_item) =============== =============== 
// returns the index of an item that was free, but is now allocated. If there are no more free items, returns a negative number
int allocItem(BlockMap* b) {
	for (int i = 0; i < b->count; i++) {
		if (!GET_BIT(b->buffer, i)) {
			SET_BIT(b->buffer, i);
			return i;
		}
	}
	return -1;
}

// =============== =============== BlockMap (Free_item) =============== =============== 
// frees the item at location i, first checking that it wasn't already free. Returns 0 on success, <0 if there was an error
int freeItem(BlockMap* b, int i) {
	if (!GET_BIT(b->buffer, i)) {
		printf("oops - freeing an item that is already marked free\n");
		return -1;
	}
	CLEAR_BIT(b->buffer, i);
	return 0;
}

int getFileSize(int f) {
	int ret = lseek(f, 0, SEEK_END);
	lseek(f,0,SEEK_SET);
	return ret;
}

// =============== =============== BlockMap (Read) =============== =============== 
// Reads, from a BlockDevice, a BlockMap into the memory.  
BlockMap* readBlockMap(block_device_t bd,disk_addr_t b_map_address){
	// How many bytes do we need to read for the block map?
	// bytes_per_blockmap/bytes_per_block = (blocks_per_blockmap)
	int bytes_per_blockmap = bd->m_blockCount / 8; 

	BlockMap_p b = allocBlockMap(bd->m_blockCount);
	b->count = bd->m_blockCount; 
	int num_read = readBlock(bd, b_map_address,b->buffer,bytes_per_blockmap); 
	assert(num_read == 0);
	return b; 
}


// =============== =============== BlockMap (Write) =============== =============== 
// writes Block Map to a Block Device 
int writeBlockMap(block_device_t bd,BlockMap* b,disk_addr_t b_map_address){
	// recall: disk address is the number of blocks between the start of the disk and the block in question
	
	// How many bytes do we need to write for the block map? 
	// bytes_per_blockmap/bytes_per_block = (blocks_per_blockmap)
	int bytes_per_blockmap = bd->m_blockCount / 8; 

	int wb = 0; 
	while (wb <= bytes_per_blockmap) {
		// Is the block map bigger than a block?   
		if (writeBlock(bd, b_map_address, b->buffer) == 0){
			wb += bd->m_bytesPerBlock;
			// If we have to move to a new block, increase the block map address
			// to represent the new position. 
			b_map_address += 1; 
		} else {
			fprintf(stderr, "Write error in writeBlockMap\n");
			return -1; 
		}
	}
	return 0; 
}


// =============== =============== BlockMap (Print) =============== =============== 
// Prints a BlockMap. 
void printBlockMap(BlockMap *b){
	for (int i = 0; i < b->count; i++ ){
        if (getBit(b, i)) {
            printf("%d", 1);
        } else {
            printf("%d", 0);
        }
        
    } 
    printf("\n"); 
}
