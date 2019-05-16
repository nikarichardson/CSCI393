#include "block_cache.h"

// allocates and returns a new block cache
block_cache_t allocateBlockCache(block_device_t bd, int bufferCacheCount) {
    block_cache_t ret = (block_cache_t) calloc(1, sizeof(BlockCache));
    ret->count = bufferCacheCount;
    ret->blockDevice = bd;

    ret->cacheArray = (block_cache_entry_t *) calloc(bufferCacheCount, sizeof(BlockCacheEntry));
    for (int i = 0; i < ret->count; i++) {
        ret->cacheArray[i]->buffer = calloc(bd->m_bytesPerBlock, 1);
    }
    return ret;
}

// frees the memory associated with a block cache
void destroyBlockCache(block_cache_t bc) {
    for (int i = 0; i < bc->count; i++) {
        free(bc->cacheArray[i]->buffer);
    }
    free(bc->cacheArray);
    free(bc);
}

// internal helper for getCachedBlock
block_cache_entry_t getCacheEntry(block_cache_t bc, disk_addr_t addr) {
    for (int i = 0; i < bc->count; i++) {
        if (bc->cacheArray[i]->blockNum == addr) {
            return bc->cacheArray[i];
        }
    }
    return NULL;
}

// if a block is cached, return its buffer
// if it isn't currently cached, return NULL
char * getCachedBlock(block_cache_t bc, disk_addr_t addr) {
    block_cache_entry_t bce = getCacheEntry(bc, addr);
    return (bce == NULL) ? NULL : bce->buffer;
}

// returns a usable cache block
// if none available, reclaims a clean cache block
// if no clean blocks available, cleans one and returns it
block_cache_entry_t allocCacheBlock(block_cache_t bc, int blockNum) {
    for (int i = 0; i < bc->count; i++) {
        bc->roundRobinNext = (bc->roundRobinNext + 1) % bc->count;
        block_cache_entry_t bce = bc->cacheArray[bc->roundRobinNext];
        if (false == bce->isDirty) {
            bce->blockNum = blockNum;
            bzero(bce->buffer, bc->blockDevice->m_bytesPerBlock); // don't do this when not needed?
            return bce;
        }
    }

    // if we've gotten this far without returning, we need to clean a
    // block and return it.
    block_cache_entry_t bce = bc->cacheArray[bc->roundRobinNext];
    // write that block to disk
    writeBlock(bc->blockDevice, bce->blockNum, bce->buffer);
    bce->blockNum = blockNum;
    bzero(bce->buffer, bc->blockDevice->m_bytesPerBlock); // don't do this when not needed?
    return bce;
}

block_cache_entry_t doCacheBlock(block_cache_t bc, int blockNum) {
    // get a cache entry
    block_cache_entry_t bce = allocCacheBlock(bc, blockNum);
    bce->blockNum = blockNum;
    bce->isDirty = false;
    // read block
    readBlock(bc->blockDevice, blockNum, bce->buffer);
    return bce;
}
