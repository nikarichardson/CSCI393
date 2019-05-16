#pragma once

#include "inode.h"
#include "block_device.h"
#include "block_cache.h"
#include "dylan_bit_set.h"
#include "master_block.h"

typedef struct DirectoryEntry *directory_cache_t;

typedef struct FileSystem {
    block_device_t     block_device;
    master_block_t     master_block;  
    bit_set_t          block_map;
    inode_map_t        inode_map;
    directory_cache_t  root_dir;   // this is also our Directory Cache
    // TODO: block_cache_t  block_cache;
} FileSystem, *FileSystem_t, *file_system_t;

typedef enum SeekType {
    SeekSet,
    SeekCur,
    SeekEnd
} SeekType;

typedef struct File {
    INode_t      inode;
    int          offset;
    FileSystem_t fs;
} File, *file_t;

int newfs(char *device_filename, int block_size, int block_count, int inode_count);

// mounts a filesystem, returns a pointer to it if successful,
// or NULL if unsuccessful
file_system_t mount(char *device_filename);

// unmounts a filesystem. No return value - there's not much you can
// do to recover it it fails.
void unmount(file_system_t fs);

// TODO:
// Take a path and return an INode_t of the inode at that path
// or NULL
INode_t fs_namei(file_system_t fs, char *path);

// TODO:
// create a directory at path, returns 0 on success, -1 on error
int fs_mkdir(file_system_t fs, char *name, int mode);

// TODO:
// create a link from the inode located at frompath to the directory +
// filename at topath. Increments the link count in the source inode.
// returns 0 on success, -1 on error
int fs_link(file_system_t fs, const char *frompath, const char *topath);

// TODO:
// unlinks the inode at path (if there is one), returns 0 on success,
// -1 on error.
int fs_unlink(file_system_t fs, char *path);

// TODO:
// opens a file for reading or writing. Returns a newly-allocated
// File handle structure. The seek position is initialized to 0.
File *fs_open(file_system_t fs, const char *path);

// TODO:
// closes a file, releases the file handle
void fs_close(File *f);

// TODO:
// reads byte_count bytes from f at the current seek position into buf.
// Returns the number of bytes read (or -1 on error).
// The seek position is incremented by the bytes read.
int fs_read(File *f, char *buf, int byte_count);

// TODO:
// writes byte_count bytes to f at the current offset into buf.
// Returns the number of bytes written (or -1 on error).
// Seek position is incremented by bytes written.
int fs_write(File *f, char *buf, int byte_count);

// TODO:
// Updates seek position of file pointer.
// If whence is SeekSet, seek position is the beginning + offset
//              SeekCur, seek position is current + offset
//              SeekEnd, seek position is size + offset
void fs_lseek(File *f, int offset, int whence);

/* ********************************************************************* */
// Below here are internal functions, only for filesystem
// implementors, not clients.
disk_addr_t getDiskAddressOfBlock(INode_t inode, block_offset_t b, bool alloc_if_absent, file_system_t fs);

// reads num_bytes from inode, starting @start. Returns number of bytes read
int iNodeRead(INode_t inode, byte_offset_t start, int num_bytes, char *buffer, file_system_t fs);

// writes num_bytes to inode, starting @start. Returns number of bytes written
int iNodeWrite(INode_t inode, byte_offset_t start, int num_bytes, char *buffer, file_system_t fs);

INode * allocateINodeMap(int num_inodes, bool init);
INodeAddr_t allocateINode(file_system_t fs);
void freeINode(file_system_t fs, INodeAddr_t i);
INode * getINode(FileSystem_t fs, INodeAddr_t i);

int writeINodeMap(block_device_t bd, INode_t inm, int disk_addr, int inode_count);
int readINodeMap(block_device_t bd, INode_t inm, int disk_addr, int inode_count);

// Utility functions:
int breakWords(char *in, char **out, int max_words, const char *delim);

