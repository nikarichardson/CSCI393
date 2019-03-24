#pragma once

#include <stdint.h>
#include "block_device.h"

#define MY_MAGIC_NUM 0xF00DCAFE

typedef int disk_addr_t;

typedef struct MasterBlock {
    uint64_t    magic_number;
    int         bytes_per_block;
    int         block_count;        			// blocks on this device
    disk_addr_t block_map_address;
    disk_addr_t inode_map_address;
} MasterBlock, *master_block_t;

master_block_t allocMasterBlock ( int bytes_per_block
                                , int block_count
                                , disk_addr_t block_map_address);

void freeMasterBlock(master_block_t mb);

block_device_t bootstrapDevice(char *deviceName);

master_block_t readMasterBlock(block_device_t bd, disk_addr_t mbloc);

int writeMasterBlock(block_device_t bd, master_block_t mb, disk_addr_t mbloc);
