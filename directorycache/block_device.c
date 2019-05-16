// API for raw access to a block device.
// For the class, the block device is going to be represented by a
// file on the host operating system. With very minor tweaks, it can
// be directed to a real block device on a Unix system.

// Methods:
// open - opens a block device
// close - closes the device
// read_block - takes a block number and a buffer - reads that block into the buffer
// write_block - takes a block number and a buffer - writes the block

// Public attributes:
// block_size - number of bytes per block on this device
// block_count - number of blocks on this device

#include "block_device.h"
#include <assert.h>

// This function creates a new block device, possibly creating a new
// file, truncating or exending an existing one.
// deviceName is the name of the file being created.
// blockSize is the bytes per block
// blockCount is the number of blocks for the device
block_device_t createBlockDevice(char * deviceName, int blockSize, int blockCount) {
    block_device_t ret = calloc(1, sizeof(BlockDevice));
    ret->m_bytesPerBlock = blockSize;
    ret->m_blockCount = blockCount;
    ret->m_deviceHandle = open(deviceName, O_RDWR | O_CREAT, 0644);
    // octcal 644 is owner read/write, everyone else read-only - see 'man chmod'
    if (ret->m_deviceHandle < 0) {
        char *desc = strerror(errno);
        fprintf(stderr, "error creating device file %s due to %s\n", deviceName, desc);
        return NULL;
    }
    int truncResult = ftruncate(ret->m_deviceHandle, blockSize * blockCount);
    if (truncResult != 0) {
        fprintf(stderr, "error setting file size\n");
        return NULL;
    }
    return ret;
}

// Opening a device that has had a master block written to it takes
// two steps: first open the device, which this function does.
// Returns a newly allocated block_device_t
// After this function, setupDevice also needs to set the block size /
// count before this device can be used
block_device_t openBlockDevice(char * deviceName) {
    block_device_t ret = calloc(1,sizeof(BlockDevice));
    assert(ret && "calloc failed in openBlockDevice!?");
    ret->m_deviceHandle = open(deviceName, O_RDWR, 0644);
    if (ret->m_deviceHandle < 0) {
        char *desc = strerror(errno);
        fprintf(stderr, "error opening device file %s due to %s\n", deviceName, desc);
        free(ret);
        return NULL;
    }
    return ret;
}

// the second half of opening a block device is for the Master Block
// functions to set the block count and block size. After this
// function is called, the block device is ready to go.
void setupBlockDevice(block_device_t bd, int blockCount, int bytesPerBlock) {
    bd->m_blockCount = blockCount;
    bd->m_bytesPerBlock = bytesPerBlock;
}

// closes a device, frees the memory for the BlockDevice structure
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
int readBlock(block_device_t bd, int blockNum, char *buff) {
    int byteOffset = blockNum * bd->m_bytesPerBlock;
    int seekRet = lseek(bd->m_deviceHandle, byteOffset, SEEK_SET);
    if (seekRet != byteOffset) {
        fprintf(stderr, "seek error in readBlock\n");
        return -1;
    }
    int numRead = read(bd->m_deviceHandle, buff, bd->m_bytesPerBlock);
    if (numRead != bd->m_bytesPerBlock) {
        // raise some heck here - should never happen!
        fprintf(stderr, "read error in readBlock\n");
        return -1;
    }
    return 0;
}

// Special function for bootstrapping the block device -
// allows you to read a non-blocksize # of bytes
int readFirstBytes(block_device_t bd, char *buffer, int numBytes) {
    lseek(bd->m_deviceHandle, 0, SEEK_SET);
    int ret = read(bd->m_deviceHandle, buffer, numBytes);
    return ret;
}

// writes data pointed to by buffer to the block device at blockNum
// address. Returns 0 on success, -1 on failure
int writeBlock(block_device_t bd, int blockNum, const char *buff) {
    int byteOffset = blockNum * bd->m_bytesPerBlock;
    int seekRet = lseek(bd->m_deviceHandle, byteOffset, SEEK_SET);
    if (seekRet != byteOffset) {
        fprintf(stderr, "seek error in writeBlock\n");
        return -1;
    }
    int numWritten = write(bd->m_deviceHandle, buff, bd->m_bytesPerBlock);
    if (numWritten != bd->m_bytesPerBlock) {
        fprintf(stderr, "write error in readBlock\n");
        return -1;
    }
    return 0;
}
