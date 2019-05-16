#include "inode.h"

#include <string.h>
#include <stdbool.h>
#include "filesystem.h"
#include "dylan_bit_set.h"

// reads num_bytes from inode, starting @start, into buffer. Returns number of bytes read
int iNodeRead(INode_t inode, byte_offset_t start, int num_bytes, char *buffer, file_system_t fs) {
    // give things some short (but clear) names
    int bytesPerB = fs->block_device->m_bytesPerBlock;
    int firstBlock = floorDiv(start, bytesPerB);
    int lastBlock = floorDiv(start + num_bytes, bytesPerB);
    int numBlocks = lastBlock - firstBlock + 1; // be careful with fenceposts!
    // offset within the first block we're reading in
    int blockOffset = start - blocksToBytes(firstBlock, fs->block_device);
    int buffOffset = 0;
    for (int i = 0; i < numBlocks; i++) {
        // byteCount handles the possibly less-than bytesPerBlock
        // reads of the first (bytesPerB-blockOffset) and
        // last (num_bytes - buffOffset) blocks being read.
        int byteCount = min(bytesPerB - blockOffset, num_bytes - buffOffset);

        // copy byteCount bytes from blockOffset .. blockOffset + bytecount into buffer
        char tbuf[bytesPerB];
        // where is this block on disk?
        disk_addr_t diskAddr = getDiskAddressOfBlock(inode, i, false, fs);
        if (diskAddr < 0) {
            // this block is inside the inode, but not on the device
            // in this case, we just zero the buffer
            bzero(tbuf, bytesPerB);
        } else {
            // fetch from the block device
            // TODO, go through the buffer cache
            int zok = readBlock(fs->block_device, diskAddr, tbuf);
            if (zok != 0) {
                return buffOffset; // this indicates an error, bd reported it
            }
        }
        // copy the data from the device buffer to the user's buffer
        for (int ci = 0; ci < byteCount; ci++) {
            buffer[buffOffset + ci] = tbuf[blockOffset + ci];
        }

        buffOffset += byteCount;
        blockOffset = 0;
    }
    return buffOffset;
}

// writes num_bytes to inode, starting @start. Returns number of bytes written
int iNodeWrite(INode_t inode, byte_offset_t start, int num_bytes, char *buffer, file_system_t fs) {
    // give things some short (but clear) names
    int bytesPerB = fs->block_device->m_bytesPerBlock;
    int firstBlock = floorDiv(start, bytesPerB);
    int lastBlock = floorDiv(start + num_bytes, bytesPerB);
    int numBlocks = lastBlock - firstBlock + 1; // think hard about fenceposting here
    // offset within the first block we're writing to
    int blockOffset = start - blocksToBytes(firstBlock, fs->block_device);
    int buffOffset = 0;

    for (int i = 0; i < numBlocks; i++) {
        // byteCount handles the possibly less-than bytesPerBlock
        // reads of the first (bytesPerB-blockOffset) and
        // last (num_bytes - buffOffset) blocks being read.
        int byteCount = min(bytesPerB - blockOffset, num_bytes - buffOffset);

        // compared to reads, writes of the first and last blocks are
        // tricky - because you need to read any partial blocks before
        // writing
        char tbuf[bytesPerB];
        // where is this block on disk? Since we're writing, allocate
        // if absent = true
        disk_addr_t diskAddr = getDiskAddressOfBlock(inode, i, true, fs);
        if (diskAddr < 0) {
            // the device is full!
            return buffOffset; // reports an error
        } else {
            // fetch from the block device
            // TODO, go through the buffer cache
            // TODO2, only read first if we're writing a partial block
            int zok = readBlock(fs->block_device, diskAddr, tbuf);
            if (zok != 0) {
                return buffOffset; // this indicates an error, bd reported it
            }
        }
        // copy the data from the user's buffer to the block buffer
        for (int ci = 0; ci < byteCount; ci++) {
            tbuf[blockOffset + ci] = buffer[buffOffset + ci];
        }
        // now write the block buffer to the device
        int zok = writeBlock(fs->block_device, diskAddr, tbuf);
        if (zok != 0) {
            return buffOffset; // this indicates an error, bd reported it
        }

        buffOffset += byteCount;
        blockOffset = 0;
    }
    // update the length, since we may have extended the file
    if (start + buffOffset > inode->num_bytes) {
        inode->num_bytes = start + buffOffset;
    }
    return buffOffset;
}

// Allocates an inode, returns its index.
// returns 0 on failure.
INodeAddr_t allocateINode(file_system_t fs) {
    for (int i = 0; i < fs->master_block->inode_count; i++) {
        if (fs->inode_map[i].status == FreeStatus) {
            fs->inode_map[i].status = AllocatedStatus;
            fs->inode_map[i].owner_uid = 0xcafef00d;
            return i;
        }
    }
    fprintf(stderr,"out of inodes");
    return 0;
}

void freeINode(file_system_t fs, INodeAddr_t i) {
    assert(fs->inode_map[i].status != FreeStatus && "trying to free an already free inode");
    assert(fs->inode_map[i].link_count == 0 && "freeing an inode with link_count != 0");
    fs->inode_map[i].owner_uid = 0xfeedfeed;
    fs->inode_map[i].status = FreeStatus;
}

INode * allocateINodeMap(int num_inodes, bool init) {
    assert (num_inodes > 1);
    INode *ret = calloc(num_inodes, sizeof(INode));
    if (init) {
        for (int i = 0; i < num_inodes; i++) {
            ret[i].inode_num = i;
            ret[i].status    = FreeStatus;
            ret[i].owner_uid = 0x1337f337;
        }
    }
    return ret;
}

int writeINodeMap(block_device_t bd, INode_t inm, int disk_addr, int inode_count) {
    int bytes_in_inode_map = inode_count * sizeof(INode);
    int blocks_in_inode_map = ceilDiv(bytes_in_inode_map, bd->m_bytesPerBlock);
    for (int i = 0; i < blocks_in_inode_map; i++) {
        char *buf_addr = (char *)inm + (i * bd->m_bytesPerBlock);
        int zok = writeBlock(bd, disk_addr+i, buf_addr);
        if (zok != 0) {
            fprintf(stderr, "unable to write inode map");
            return -1;
        }
    }
    // debug: printf("wrote %d blocks of inode map @%d\n", blocks_in_inode_map, disk_addr);
    return 0;
}

int readINodeMap(block_device_t bd, INode_t inm, int disk_addr, int inode_count) {
    int bytes_in_inode_map = inode_count * sizeof(INode);
    int blocks_in_inode_map = ceilDiv(bytes_in_inode_map, bd->m_bytesPerBlock);
    for (int i = 0; i < blocks_in_inode_map; i++) {
        char *buf_addr = (char *)inm + (i * bd->m_bytesPerBlock);
        int zok = readBlock(bd, disk_addr+i, buf_addr);
        if (zok != 0) {
            fprintf(stderr, "unable to write inode map");
            return -1;
        }
    }
    return 0;
}


// the internal, recursive version of gDAOB, but for now only handles
// level 0 INodes
disk_addr_t getDiskAddressOfBlockRecursive(INode_t inode, block_offset_t b
                                          , bool alloc_if_absent, int level
                                          , file_system_t fs) {
    if (level == 0) {
        if (b < BLOCK_PTRS_PER_INODE_STRUCT) {
            if (inode->block_ptrs[b] > 0) {
                return (inode->block_ptrs[b]);
            } else if (alloc_if_absent) {
                inode->block_ptrs[b] = allocateBlock(fs->block_map);
                return (inode->block_ptrs[b]);
            } else {
                assert(false && "getdiskAddressofBlock"); 
                fprintf(stderr, "inode: getdiskAddressofBlock error\n");
                return -1;
            }
        } else {
            fprintf(stderr, "we don't support INodes that big (yet), (%d > %d)\n", b, BLOCK_PTRS_PER_INODE_STRUCT);
            return -1;
        }
    } else {
        fprintf(stderr, "we don't support INodes with level > 0 (yet)\n");
        return -1;
    }
}

// disk_addr_t diskAddr = getDiskAddressOfBlock(inode, i, true, fs);

// getDiskAddressOfBlock - is the main task of an iNode: map file offsets to disk
// addresses. The alloc_with_absent flag used for writes to previously unallocated blocks.
// returns a disk address of the block of data if present or if alloc_if_absent,
// or -1 otherwise
disk_addr_t getDiskAddressOfBlock(INode_t inode, block_offset_t b
                                    , bool alloc_if_absent, file_system_t fs) {
    assert(inode && inode->level >= 0);
    return getDiskAddressOfBlockRecursive(inode, b, alloc_if_absent, inode->level, fs);
}

int max(int a, int b) {
    return (a >= b ? a : b);
}

int min(int a, int b) {
    return (a <= b ? a : b);
}
