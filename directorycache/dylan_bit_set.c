#include "dylan_bit_set.h"

BitSet* allocBitSet(int num_bits, int block_size) {
    int bytes_in_bitset = sizeof(BitSet) + ceilDiv(num_bits, 8);
    int blocks_in_bitset = ceilDiv(bytes_in_bitset, block_size);
    bytes_in_bitset = blocks_in_bitset * block_size;
    bit_set_t ret = calloc(1, bytes_in_bitset);
    ret->count = num_bits;
    ret->bitset_magic = BITSET_MAGIC;
    return ret;
}

// frees a BitSet
void freeBitSet(BitSet* bs) {
    free(bs);
}

// sets bit i of the BitSet
void setBit(BitSet* b, int i) {
    SET_BIT(b->bytes, i);
}

// clears bit i of the BitSet
void clearBit(BitSet* b, int i) {
    CLEAR_BIT(b->bytes, i);
}

// returns the bit (boolean) value of the ith bit of the BitSet
bool getBit(BitSet* b, int i) {
    return GET_BIT(b->bytes, i);
}

// =================================================
// Now using BitSet, create an allocator interface
// =================================================
// returns the index of an item that was free, but is now allocated. If there are no more free items, returns a negative number
int allocateBlock(BitSet* b) {
    for (int i = 0; i < b->count; i++) {
        if (!GET_BIT(b->bytes, i)) {
            SET_BIT(b->bytes, i);
            return i;
        }
    }
    return -1;
}

// frees the item at location i, first checking that it wasn't already free. Returns 0 on success, <0 if there was an error
int freeBlock(BitSet* b, int i) {
    if (!GET_BIT(b->bytes, i)) {
        printf("oops - freeing an item that is already marked free\n");
        return -1;
    }
    CLEAR_BIT(b->bytes, i);
    return 0;
}

int getFileSize(int f) {
    int ret = lseek(f, 0, SEEK_END);
    lseek(f,0,SEEK_SET);
    return ret;
}

int getBlocksInBlockMap(block_device_t bd) {
    int bits_per_bitset = bd->m_blockCount;
    int bytes_per_bitset = ceilDiv(bits_per_bitset, 8);
    return ceilDiv(bytes_per_bitset, bd->m_bytesPerBlock);
}

// allocates and returns a bitset read from a block device
BitSet* readBlockMap(block_device_t bd, disk_addr_t first_block) {
    int blocks_per_bitset = getBlocksInBlockMap(bd);
    char *ret = calloc(1, blocks_per_bitset * bd->m_bytesPerBlock);
    for (int i = 0; i < blocks_per_bitset; i++) {
        char *buf = &ret[i * bd->m_bytesPerBlock];
        if (readBlock(bd, first_block + i, buf) != 0) {
            fprintf(stderr, "error reading bitset block\n");
            return NULL;
        }
    }
    BitSet *rbs = (BitSet *)ret;
    if (rbs->bitset_magic != BITSET_MAGIC) {
        fprintf(stderr, "bad magic in readBlockMap\n");
    }
    return rbs;
}

// writes Bit Set b to a block device
int writeBlockMap(block_device_t bd, BitSet *b, disk_addr_t first_block) {
    char *buf = (char *)b;
    int blocks_per_bitset = getBlocksInBlockMap(bd);
    assert(b->bitset_magic == BITSET_MAGIC);
    for (int i = 0; i < blocks_per_bitset; i++) {
        char *bbuf = &buf[i * bd->m_bytesPerBlock];
        if (writeBlock(bd, first_block + i, bbuf) != 0) {
            fprintf(stderr, "error writing bitset block\n");
            return -1;
        }
    }
    return 0;
}
