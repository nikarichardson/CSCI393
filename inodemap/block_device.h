#pragma once

#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>
#include <fcntl.h>
#include <errno.h>
#include <string.h>


/*
    The BlockDevice is the API that a file system is built on.
    Any block device supports block-level reads and writes.

    In this system, we simulate a block device using an OS file.
    In theory (an exercise for the motivated?) we could use almost
    this exact code to access an actual raw device (e.g.,
    /dev/rdiskx), but then the program would need to run as
    super-user, and if the wrong device were specified, you could
    overwrite your OS or user data. Beware.

    API overview:

    createBlockDevice creates a new, blank block device.
    The blockSize argument specifies how many bytes there are per
    block. Real world file systems have had blocks as small as 512
    bytes, and as large as 4096 bytes.

    openBlockDevice opens a block device file, but doesn't initialize
    its values - the caller needs to do that (see
    bootstrapDeviceFromMasterBlock(block_device_t bd, uint64_t magic))

    The action end of a block device are the readBlock and writeBlock
    calls. They both take a block number and a buffer. readBlock fills
    the buffer with the data from the block device @ blockNum, and
    writeBlock writes the buffer to the block device @ blockNum.

    The m_bytesPerBlock and m_blockCount members are available for
    friends, like the BlockMap.
*/

#define ceilDiv(n,d) ( (int)((n + d - 1)/d))

typedef int disk_addr_t;  // signed int, so we can have negative
                          // values for, e.g., copy-on-write

typedef struct BlockDevice {
    int m_deviceHandle;
    int m_blockCount;
    int m_bytesPerBlock;
} BlockDevice, *block_device_t;

// create a fresh block device with the given filename, bytes per
// block, and block count.
block_device_t createBlockDevice(char * deviceName, int blockSize, int blockCount);

// when you open a block device (that has been created already), all you have is its name
block_device_t openBlockDevice(char * deviceName);
// so we rely on the Master Block functions to call setupBlockDevice
// to finish assigning its parameters.
void setupBlockDevice(block_device_t bd, int blockCount, int bytesPerBlock);

// closes device, 0 is good, <0 an error occurred
int closeBlockDevice(block_device_t bd);

// readBlock and writeBlock return 0 on success, <0 on error
int readBlock(block_device_t bd, disk_addr_t blockNum, char *buff);

int writeBlock(block_device_t bd, disk_addr_t blockNum, const char *buff);

// Special function for bootstrapping the block device -
// allows you to read a non-blocksize # of bytes
int readFirstBytes(block_device_t bd, char *buffer, int numBytes);
