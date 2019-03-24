#pragma once
#include "block_device.h"
#include "master_block.h"
#include "dylan_bit_set.h"
#include "inode.h"
#include "assert.h"

int newfs(char *device_filename, int block_size, int block_count);

int ceiling(int x, int y); 
