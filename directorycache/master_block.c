#include "block_device.h"
#include "master_block.h"
#include <assert.h>

#define MY_MAGIC 0xF00DCAFE

master_block_t allocMasterBlock ( int bytes_per_block
                                , int block_count
                                , disk_addr_t block_map_address) {
    assert(bytes_per_block > 0 && "bad bytes_per_block in allocMasterBlock");
    master_block_t ret = calloc(1,bytes_per_block); // not sizeof MB!
    assert(ret && "calloc failed in allocMasterBlock");
    ret->magic_number = MY_MAGIC;
    ret->bytes_per_block = bytes_per_block;
    ret->block_count = block_count;
    ret->block_map_address = block_map_address;
    return ret;
}

void freeMasterBlock(master_block_t mb) {
    free(mb);
}

// Opens the file, checks if the magic number matches, retrieves the
// block size from and number of blocks from the device the device -
// for bootstrapping the mount process. (You need the block size to
// read from the block device) returns block_device_t on success,
// NULL on failure (usually it's because magic didn't match)
block_device_t bootstrapDevice(char *deviceName) {
    block_device_t bd = openBlockDevice(deviceName);
    MasterBlock tempMaster;
    int bytesRead = readFirstBytes(bd, (char *)&tempMaster, sizeof(MasterBlock));
    if (bd == NULL || bytesRead != sizeof(MasterBlock)) {
        fprintf(stderr,"unable to read master block to determine block size\n");
        return NULL;
    }
    if (tempMaster.magic_number != MY_MAGIC) {
        fprintf(stderr,"bad magic in getBlockSize\n");
        return NULL;
    }
    setupBlockDevice(bd, tempMaster.block_count, tempMaster.bytes_per_block);
    return bd;
}

master_block_t readMasterBlock(block_device_t bd, disk_addr_t mbloc) {
    char * mb = calloc(1, bd->m_bytesPerBlock);
    int check = readBlock(bd, mbloc, mb);
    if (check != 0) {
        fprintf(stderr,"readBlock failed in readMasterBlock");
        return NULL;
    }
    return (master_block_t) mb;
}

int writeMasterBlock(block_device_t bd, master_block_t mb, disk_addr_t mbloc) {
    return writeBlock(bd, mbloc, (char *) mb);
}
