#pragma once

#include "inode.h"
#include "filesystem.h"
#include <stdbool.h>

#define MAX_DIR_ENTRY_LEN 256
#define MAX_DIR_NAME_LEN 25

// A directory is a mapping from Name -> INode. 
typedef struct DirectoryEntry {
    INode_t                    inode_ptr;          // this inode
    char *                     name;               // the name for this inode in this directory
    struct DirectoryEntry     *next_sibling;       // siblings in a directory are in a linked list
    struct DirectoryEntry     *maybe_children;     // for directories
    bool                       is_dirty;           // directory needs to be written to disk
} DirectoryEntry, *DirectoryEntry_t, *directory_entry_t;

// allocates and returns a new DirectoryEntry for an INode
void             addChild(DirectoryEntry_t parent, char *name, INode_t inode);
// if dir is cached, returns its children
// if it is not cached, reads it from its inode, and returns its
// children
DirectoryEntry_t getChildren(DirectoryEntry_t dir, FileSystem_t fs);
// writes a directory (the pairs of name/inode_num of its children) to its inode
void            writeDirectory(DirectoryEntry_t d, FileSystem_t fs);
void             flushDirectoryCache(DirectoryEntry_t dir, FileSystem_t fs);

// utility functions:
// counts # of c's in buf
int countOccurrences(char *buf, char c, int bsize);

// special case directory entry function
void addRoot(FileSystem_t fs, INode_t inode);
