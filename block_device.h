#ifndef BLOCKDEVICE_H
#define BLOCKDEVICE_H
#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>
#include <fcntl.h>
#include <errno.h>
#include <stdbool.h>
#include <string.h>
#include <assert.h>

#define ceilDiv(n,d) ( (int)((n + d - 1)/d))
#define BLOCKMAP
#define BLOCKS_PER_DEVICE 100
#define BLOCKSIZE 1024 // weird BLOCKMAP macro here  
#define SET_BIT(cs, i)   ((cs[i/8]) |= (1 << (i % 8)))
#define CLEAR_BIT(cs, i) ((cs[i/8]) &= ~(1 << (i % 8)))
#define GET_BIT(cs, i) (((cs[i/8]) & (1 << (i % 8))) != 0)

typedef int disk_addr_t;  // signed int, so we can have negative
						  // values for, e.g., copy-on-write

// =================================================
// Block Device
// =================================================
typedef struct BlockDevice {
	char * deviceName; 
	int m_deviceHandle;
	int m_blockCount;
	int m_bytesPerBlock;
} BlockDevice, *block_device_t;

typedef struct Devices {
    block_device_t dev;
    struct Devices * next; 
} devices_t; 

block_device_t createBlockDevice(char * deviceName, int blockSize, int blockCount);

// so we rely on the Master Block functions to call setupBlockDevice
// to finish assigning its parameters.
void setupBlockDevice(block_device_t bd, int blockCount, int bytesPerBlock);

// Special function for bootstrapping the block device -
// allows you to read a non-blocksize # of bytes
int readFirstBytes(block_device_t bd, char *buffer, int numBytes);

// when you open a block device (that has been created already), all you have is its name
block_device_t openBlockDevice(char * deviceName);

// closes device, 0 is good, <0 an error occurred
int closeBlockDevice(block_device_t bd);

int readBlock(block_device_t bd, int blockNum, char *buff, int read_bytes);

int writeBlock(block_device_t bd, int blockNum, const char *buff);

#endif /* BLOCKDEVICE_H */

