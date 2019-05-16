#pragma once

#include <time.h>
#include <stdbool.h>
#include <stdint.h>
#include "block_device.h"

// index in the INode Map
typedef int INodeAddr_t;
// A block offset is a block address within an inode.
typedef int block_offset_t;
// a byte offset is an offset within an inode
typedef int byte_offset_t;
typedef time_t timestamp_t;

int max(int a, int b);
int min(int a, int b);

#define BLOCK_PTRS_PER_INODE_STRUCT 16

typedef enum INodeStatus {
    UnusedStatus, // let's not have 0 be valid
    AllocatedStatus,
    FreeStatus
} inode_status_t;

typedef enum INodeType {
    UnusedType,
    FileType,
    DirectoryType,
    SymlinkType,
    PipeType
} inode_type_t;

typedef struct INode {
    INodeAddr_t    inode_num;  // which inode this is (index in the inode map)
    uint32_t       owner_uid;  // who owns this
    uint32_t       gid;        // which group id the perms refer to
    inode_type_t   type;       // file, directory, symlink, ...
    uint16_t       perms;      // RWX permissions for owner / group / all
    inode_status_t status;     // whether it's allocated, needs to be written, etc
    uint16_t       link_count; // how many hard links there are to this INode
    timestamp_t    cdate;      // creation_time
    timestamp_t    mdate;      // most recent modification time
    uint16_t       level;      // level
    uint64_t       num_bytes;  // the current size of the inode
    disk_addr_t    block_ptrs[BLOCK_PTRS_PER_INODE_STRUCT]; // data blocks, or blocks of disk_address_t[]
} INode, *INode_t, *inode_map_t;

