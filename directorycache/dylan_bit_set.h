#pragma once

#include <stdlib.h>
#include <stdio.h>
#include <stdbool.h>
#include <unistd.h>
#include <fcntl.h>
#include <assert.h>

#include "block_device.h"

#define BITSET_MAGIC 0xB175E700

typedef struct BitSet {
    int bitset_magic;
    int count;
    char bytes[1];
} BitSet, *bit_set_t;

#define SET_BIT(cs, i)   ((cs[i/8]) |= (1 << (i % 8)))
#define CLEAR_BIT(cs, i) ((cs[i/8]) &= ~(1 << (i % 8)))
#define GET_BIT(cs, i) (((cs[i/8]) & (1 << (i % 8))) != 0)

BitSet* allocBitSet(int num_bits, int block_size);

// frees a BitSet
void freeBitSet(BitSet* bs);

// sets bit i of the BitSet
void setBit(BitSet* b, int i);

// clears bit i of the BitSet
void clearBit(BitSet* b, int i);

// returns the bit (boolean) value of the ith bit of the BitSet
bool getBit(BitSet* b, int i);

// =================================================
// Now using BitSet, create an allocator interface
// =================================================
// returns the index of an item that was free, but is now allocated. If there are no more free items, returns a negative number
int allocateBlock(BitSet* b);

// frees the item at location i, first checking that it wasn't already free. Returns 0 on success, <0 if there was an error
int freeBlock(BitSet* b, int i);

int getFileSize(int f);

// reads and returns, from a block device, a Bit Set into the memory pointed to by b.
BitSet* readBlockMap(block_device_t bd, disk_addr_t first_block);

// writes Bit Set b to a block device
int writeBlockMap(block_device_t bd, BitSet *b, disk_addr_t first_block);

// return the number of device blocks required to store the BlockMap
// for this device
int getBlocksInBlockMap(block_device_t bd);
