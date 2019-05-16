#pragma once

#include <stdbool.h>
#include "block_device.h"

// A block cache entry knows which block number it's a cache for,
// whether it is dirty (written to cache, but not the block device)
// and the memory cache of its contents.
typedef struct BlockCacheEntry {
    disk_addr_t  blockNum;
    bool         isDirty;
    char         *buffer;
} BlockCacheEntry, *block_cache_entry_t;

// the block cache knows which device it's a cache of, how many blocks
// it has a cache for, and its array of cache entry elements.
typedef struct BlockCache {
    block_device_t      blockDevice;
    int                 count;
    int                 roundRobinNext;
    block_cache_entry_t *cacheArray;
} BlockCache, *block_cache_t;

// create & destroy a block cache
block_cache_t allocateBlockCache(block_device_t bd, int bufferCacheCount);
void destroyBlockCache(block_cache_t bc);

// return the cache for block @addr, or NULL if it's not yet cached
char * getCachedBlock(block_cache_t bc, disk_addr_t addr);

// write all of the cached/dirty blocks back to the block device
// returns True if successful, False (and prints to stderr why) on error
bool flushBlockCache(block_cache_t bc, block_device_t bd);

// when a block is not cached (getCachedBlock returns null),
// this method is used to make it cached
// returns cache entry on success, or NULL (and prints to stderr) on failure
block_cache_entry_t doCacheBlock(block_cache_t bc, int blockNum);
