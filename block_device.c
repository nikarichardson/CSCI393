// Block Device

#include "block_device.h"
#include "master_block.h"

#include <stdlib.h>
#include <unistd.h>
#include <errno.h>
#include <string.h>
#include <assert.h>
#include <stdbool.h>

#define MAGIC 0xFEEDC0DE
#define BLOCKSIZE 1024
#define BLOCKS_PER_DEVICE 100


// creates a new block device, possibly creating a new
// file, truncating or extending an existing one.
// deviceName is the name of the file being created.
// blockSize is the bytes per block
// blockCount is the number of blocks for the device aka the Blocks Per Device in MasterBlock 
// =============== =============== BLOCK DEVICE: A P I =============== =============== 
// =============== =============== BlockDevice (Create) =============== =============== 
block_device_t createBlockDevice(char * deviceName, int blockSize, int blockCount) {
	block_device_t ret = malloc(sizeof(BlockDevice));
	ret->deviceName = deviceName; 
	ret->m_blockCount = blockCount;
	ret->m_bytesPerBlock = blockSize;
	ret->m_deviceHandle = open(deviceName, O_RDWR | O_CREAT, 0644);
	// octcal 644 is owner read/write, everyone else read-only - see 'man chmod'
	if (ret->m_deviceHandle < 0) {
		char *desc = strerror(errno);
		fprintf(stderr, "Error creating device file %s due to %s\n", deviceName, desc);
		return NULL;
	}
	int truncResult = ftruncate(ret->m_deviceHandle, blockSize * blockCount);
	if (truncResult != 0) {
		fprintf(stderr, "Error setting file size\n");
		return NULL;
	}
	return ret;
}

// Opening a device that has had a master block written to it takes
// two steps: first open the device, which this function does.
// =============== =============== BlockDevice (Open) =============== =============== 
block_device_t openBlockDevice(char * deviceName) {
    block_device_t ret = calloc(1,sizeof(BlockDevice));
    ret->m_deviceHandle = open(deviceName, O_RDWR, 0644);
    if (ret->m_deviceHandle < 0) {
        char *desc = strerror(errno);
        fprintf(stderr, "error creating device file %s due to %s\n", deviceName, desc);
        free(ret);
        return NULL;
    }
    return ret;
}

// closes a device, frees the memory for the BlockDevice structure
// =============== =============== BlockDevice (Close) =============== =============== 
int closeBlockDevice(block_device_t bd) {
    if (bd->m_deviceHandle) {
        int ok = close(bd->m_deviceHandle);
        if (ok != 0) {
            fprintf(stderr, "error closing device %s\n", strerror(errno));
            return -1;
        } else {
            bd->m_deviceHandle = 0;
        }
    }
    free(bd);
    return 0;
}


// reads data into memory pointed to by buffer from the block device at blockNum
// Returns 0 on success, -1 on failure
// readBlock fills the buffer with the data from the block device @ blockNum, and
// =============== =============== BlockDevice (Read) =============== =============== 
int readBlock(block_device_t bd, int blockNum, char *buff, int read_bytes) {
	int byteOffset = blockNum * bd->m_bytesPerBlock;
	int seekRet = lseek(bd->m_deviceHandle, byteOffset, SEEK_SET);
	if (seekRet != byteOffset) {
		fprintf(stderr, "Seek error in readBlock.\n");
		return -1;
	}

	int numRead = read(bd->m_deviceHandle, buff, read_bytes);
	if (numRead != read_bytes) {
		fprintf(stderr, "Read error in readBlock.\n");
		return -1;
	}
	return 0;
}

// writes data pointed to by buffer to the block device at blockNum
// address. Returns 0 on success, -1 on failure
// writeBlock writes the buffer to the block device @ blockNum.
// =============== =============== BlockDevice (Write) =============== =============== 
int writeBlock(block_device_t bd, int blockNum, const char *buff) {
	int byteOffset = blockNum * bd->m_bytesPerBlock;
	int seekRet = lseek(bd->m_deviceHandle, byteOffset, SEEK_SET);
	if (seekRet != byteOffset) {
		fprintf(stderr, "Seek error in writeBlock.\n");
		return -1;
	}
	int numWritten = write(bd->m_deviceHandle, buff, bd->m_bytesPerBlock);
	if (numWritten != bd->m_bytesPerBlock) {
		fprintf(stderr, "Write error in readBlock\n");
		return -1;
	}
	return 0;
}


// the second half of opening a block device is for the Master Block
// functions to set the block count and block size. After this
// function is called, the block device is ready to go.
// =============== =============== BlockDevice (Setup) =============== =============== 
void setupBlockDevice(block_device_t bd, int blockCount, int bytesPerBlock) {
    bd->m_blockCount = blockCount;
    bd->m_bytesPerBlock = bytesPerBlock;
}

// Special function for bootstrapping the block device -
// allows you to read a non-blocksize # of bytes
// =============== =============== BlockDevice (readBytes) =============== =============== 
int readFirstBytes(block_device_t bd, char *buffer, int numBytes) {
	// 0 is the address — we are trying to read MasterBlock here 
    lseek(bd->m_deviceHandle, 0, SEEK_SET);
    int ret = read(bd->m_deviceHandle, buffer, numBytes);
    return ret;
}


