#include "filesystem.h"

#include "block_device.h"
#include "master_block.h"
#include "dylan_bit_set.h"
#include "inode.h"
#include <assert.h>
#include "directory_cache.h"

int newfs(char *device_filename, int block_size, int block_count, int inode_count) {
    FileSystem fsStruct;
    FileSystem_t fs = &fsStruct;
    assert(device_filename && "NULL filename to newfs");
    BlockDevice *bd = createBlockDevice(device_filename, block_size, block_count);
    fs->block_device = bd;
    if (bd == NULL) return -1;
    if (block_size < sizeof(MasterBlock)) {
        fprintf(stderr, "block size needs to be >= sizeof(MasterBlock) (%d)\n", (int)sizeof(MasterBlock));
        return -1;
    }
    if (block_size < sizeof(INode)) {
        fprintf(stderr, "block size needs to be >= sizeof(INode) (%d)\n", (int)sizeof(INode));
        return -1;
    }
    // allocate a fresh Master Block structure
    int block_map_location = 1;
    master_block_t mb = allocMasterBlock(block_size, block_count, block_map_location);
    assert (mb && "allocMasterBlock failed");
    bit_set_t bs = allocBitSet(block_count, block_size);
    assert(bs && "allocBitSet failed");
    fs->master_block = mb;
    fs->block_map = bs;
    // mark the master block and blockmap blocks as allocated
    int blocks_in_blockmap = getBlocksInBlockMap(bd);
    int prealloc_blocks = blocks_in_blockmap + 1; // count the master block!

    // Initialize INode Map
    int bytes_per_inode = sizeof(INode);
    fs->inode_map = allocateINodeMap(inode_count, true);
    mb->inode_count = inode_count;
    assert(fs->inode_map && "allocINodeMap failed");
    mb->inode_map_address = prealloc_blocks;
    int bytes_in_inode_map = inode_count * sizeof(INode);
    int blocks_in_inode_map = ceilDiv(bytes_in_inode_map, block_size);
    printf("inode map - %d inodes, %d bytes per inode, %d bytes & %d blocks total\n",
        inode_count, bytes_per_inode, bytes_in_inode_map, blocks_in_inode_map);
    prealloc_blocks += blocks_in_inode_map;
    if (block_count <= prealloc_blocks) {
        fprintf(stderr, "block count needs to be at least Master Block + block map blocks (%d)\n", prealloc_blocks);
        return -1;
    }
    for (int i = 0; i < prealloc_blocks; i++) {
        assert(allocateBlock(bs) >= 0 && "device too small for preallocated blocks!"); // shouldn't happen - check above
    }

    // allocate the root directory
    INodeAddr_t root_dir_inode_num = allocateINode(fs);
    INode_t     root_dir_inode = getINode(fs, root_dir_inode_num);
    root_dir_inode->type = DirectoryType;
    addRoot(fs, root_dir_inode);
    fs->master_block->root_dir_inode = root_dir_inode_num;

    // write the master block to the device @ disk address 0
    if (0 > writeMasterBlock(bd, mb, 0)) {
        fprintf(stderr, "write master block failed\n");
        return -1;
    }
    // write the block map to the device starting @ disk address 1
    if (0 > writeBlockMap(bd, bs, 1)) {
        fprintf(stderr, "write block map failed\n");
        return -1;
    }
    if (0 > writeINodeMap(bd, fs->inode_map, mb->inode_map_address, inode_count)) {
        fprintf(stderr, "write inode map failed\n");
        return -1;
    }
    // root directory is thus uncached when we start
    flushDirectoryCache(fs->root_dir, fs);

    closeBlockDevice(bd);
    free(mb);
    free(bs);
    return 0;
}

file_system_t mount(char *device_filename) {
    file_system_t ret = calloc(1, sizeof(FileSystem));
    ret->block_device = bootstrapDevice(device_filename);
    if (ret->block_device != NULL) {
        // main_bd now points to a working, initialized block device
        const int mb_loc = 0;
        const int bm_loc = 1;
        if ((ret->master_block = readMasterBlock(ret->block_device, mb_loc)) != NULL &&
            ((ret->block_map = readBlockMap(ret->block_device, bm_loc)) != NULL)) {
            printf("\n%s successfully mounted\n", device_filename);
        } else {
            fprintf(stderr, "mount failed. Corrupt device?\n");
            free(ret);
            ret = NULL;
        }
    } else {
        fprintf(stderr, "open device failed. Was that the right filename?\n");
        free(ret);
        ret = NULL;
    }
    assert(ret->master_block->inode_count > 0 && "zero inodes?");
    assert(ret->master_block->inode_map_address > 1 && "bad inode map location");
    ret->inode_map = allocateINodeMap(ret->master_block->inode_count, false);
    int zok = readINodeMap(ret->block_device, ret->inode_map
                          , ret->master_block->inode_map_address
                          , ret->master_block->inode_count);
    if (zok != 0) {
        fprintf(stderr, "read inode map failed");
        free(ret);
        ret = NULL;
    }

    // add the root directory to the directory cache
    INode_t root_dir_inode = getINode(ret, ret->master_block->root_dir_inode);
    addRoot(ret, root_dir_inode);
    return ret;
}

void unmount(file_system_t fs) {
    // flush the directory cache (which may modify inodes / allocate
    // blocks
    // writing the directories to their inodes 
    flushDirectoryCache(fs->root_dir, fs);

    // write the block map to disk
    int writeZero = writeBlockMap(fs->block_device, fs->block_map, 1);

    // write the inode map
    int inmZero = writeINodeMap(fs->block_device, fs->inode_map,
                                fs->master_block->inode_map_address,
                                fs->master_block->inode_count);

    // TODO: flush the block cache when we have one
    // close the file
    int closeZero = closeBlockDevice(fs->block_device);
    if (writeZero == 0 && closeZero == 0 && inmZero == 0) {
        printf("\nunmount successful\n");
    } else {
        fprintf(stderr, "unmount error\n");
    }
}

// C doesn't have C++ (or Python)'s handy "split" function.
// breakWords takes an input string and an array of pointers to strings.
// It sets each element of the array to the next word, and returns the
// total number of words parsed. max_words is the length of the array
// of pointers.
int breakWords(char *in, char **out, int max_words, const char *delim) {
    // the first time we call strtok, we give it the buffer,
    // it returns the "newfs" command that got us here
    char *words = strtok(in, delim);
    int i = 0;
    int j = 0;
    for (; i < max_words; i++) {
        out[i] = words;
        if (words != NULL) {
            j++;
            // each subsequent call to strtok, we pass NULL (it keeps
            // a pointer into our string (!), and returns a pointer to
            // the next token
            words = strtok(NULL, delim);
        } else {
            // we're setting out[i] to NULL, which is good
        }
    }
    return j;
}

INode * getINode(FileSystem_t fs, INodeAddr_t i) {
    assert (i >= 0 && i < fs->master_block->inode_count && "bad INodeAddr to getINode");
    return &fs->inode_map[i];
}
