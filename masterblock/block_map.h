#ifndef BLOCKMAP_H
#define BLOCKMAP_H

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
// Block Map 
// =================================================
typedef struct BlockMap {
	int count;
	char *buffer;
} BlockMap, *BlockMap_p;

BlockMap* allocBlockMap(int num_bits);
// frees a BlockMap
void freeBlockMap(BlockMap* bs);
// sets bit i of the BlockMap
void setBit(BlockMap* b, int i);
// clears bit i of the BlockMap
void clearBit(BlockMap* b, int i);
// returns the bit (boolean) value of the ith bit of the BlockMap
bool getBit(BlockMap* b, int i);
// returns the index of an item that was free, but is now allocated. If there are no more free items, returns a negative number
int allocItem(BlockMap* b);
// frees the item at location i, first checking that it wasn't already free. Returns 0 on success, <0 if there was an error
int freeItem(BlockMap* b, int i);
BlockMap* createBlockMap(int number_of_blocks); 
int getFileSize(int f);
// reads, from a BlockDevice (whose name is pointed to by filename), a Block Map into the memory pointed to by b.
BlockMap* readBlockMap(block_device_t bd,disk_addr_t b_map_address);
// writes Block Map b to a Block Device
int writeBlockMap(block_device_t bd,BlockMap* b,disk_addr_t b_map_address);
// print a BlockMap 
void printBlockMap(BlockMap *b);

#endif /* BLOCKMAP_H */
