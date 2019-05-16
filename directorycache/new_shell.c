#include "block_device.h"
// TODO: include your versions of the master block and bit set headers
#include "master_block.h"
#include "dylan_bit_set.h"
#include "inode.h"
#include "filesystem.h"
#include "directory_cache.h"

#include <readline/readline.h>
#include <readline/history.h>

#include <string.h>
#include <stdbool.h>

// returns true if a has the same string value as b
bool equals(char *a, char *b, bool noprefix) {
    if (noprefix && strlen(a) != strlen(b)) {
        return false;
    }
    return !(strncmp(a,b,strlen(a)));
}

const char *delim = " \t"; // separating tokens

int main(int argc, char** argv) {
    printf("Welcome! You can exit by pressing Ctrl+C at any time...\n");

    bool done = false;
    char* buf;
    file_system_t main_filesystem = NULL;
    directory_entry_t main_current_dir = NULL;

    const int MAX_ARGS = 32;
    char *arguments[MAX_ARGS];

    while (!done && (buf = readline(">> ")) != NULL) {
        if (strlen(buf) == 0) {
            continue; // user pressed enter
        }
        add_history(buf);

        int num_words = breakWords(buf, arguments, MAX_ARGS, delim);

        if (main_filesystem == NULL) {
            ////////////////////////////////////////////////////////
            // if main_filesystem == NULL, no filesystem is mounted,
            // so the valid commands are newfs and mount (and quit)
            if (equals("newfs", arguments[0], true)) {
                if (num_words == 4) {
                    char *device_name = arguments[1];
                    // atoi is ASCII -> integer, so get the block size
                    // into an integer.
                    int block_size = atoi(arguments[2]);
                    // and now read the number of blocks
                    int block_count = atoi(arguments[3]);
                    int default_inode_count = 16; // todo - make this an optional argument
                    // now we know everything we need to create
                    // the device.
                    int newfs_ok = newfs(device_name, block_size
                                        , block_count, default_inode_count);
                    if (newfs_ok >= 0) {
                        printf("created %s with %d blocks of %d bytes per block\n", device_name, block_count, block_size);
                    } else {
                        fprintf(stderr, "error in newfs\n");
                    }
                } else {
                    fprintf(stderr, "usage: newfs <filename> <bytes per block> <block count>\n");
                }
            } else if (equals("mount", arguments[0], true)) {
                char *device_name = arguments[1];        // this should be the device name
                if (num_words == 2 && device_name != NULL) {
                    main_filesystem = mount(device_name);
                    main_current_dir = main_filesystem->root_dir;
                } else {
                    fprintf(stderr, "usage: mount <device file name>\n");
                }
            } else if (equals("q", arguments[0], false)) {
                done = true;
            } else {
                printf("valid commands: mount, newfs, quit\n");
            }
        } else {
            //////////////////////////////////////////////////
            // we have a mounted filesystem - the rest of the
            // commands work in this mode
            if (equals("q", arguments[0], false)) {
                unmount(main_filesystem);
                done = true;
            } else if (equals("unmount", arguments[0], true)) {
                unmount(main_filesystem);
                main_filesystem = NULL;
            } else if (equals("mkdir", arguments[0], true)) {
                if (num_words == 2) {
                    // make sure this directory is cached
                    getChildren(main_current_dir, main_filesystem);
                    // create the new child directory
                    INodeAddr_t new_inode_num = allocateINode(main_filesystem);
                    INode_t     new_inode = getINode(main_filesystem, new_inode_num);
                    new_inode->type = DirectoryType;
                    char *new_name = malloc(strlen(arguments[1]));
                    strcpy(new_name, arguments[1]);
                    // and add it
                    addChild(main_current_dir, new_name, new_inode);
                } else {
                    fprintf(stderr, "usage: mkdir <dir name>\n");
                }
            } else if (equals("ls", arguments[0], true)) {
                DirectoryEntry_t d = getChildren(main_current_dir, main_filesystem);
                while (d != NULL) {
                    printf("%s\t", d->name);
                    d = d->next_sibling;
                }
                printf("\n");
            } else if (equals("cd", arguments[0], true)) {
                if (num_words == 2) {
                    char *target_dir = arguments[1];
                    DirectoryEntry_t d = getChildren(main_current_dir, main_filesystem);
                    bool found = false;
                    while (d != NULL && !found) {
                        if (strcmp(d->name, target_dir) == 0) {
                            if (d->inode_ptr->type == DirectoryType) {
                                main_current_dir = d;
                                found = true;
                            } else {
                                fprintf(stderr, "cd: %s: Not a directory\n", target_dir);
                            }
                        }
                        d = d->next_sibling;
                    }
                    if (!found) {
                        fprintf(stderr, "cd: %s: no such file or directory\n", target_dir);
                    }
                } else {
                    fprintf(stderr, "usage: cd <dir_name>\n");
                }
            }

            // readline malloc's a new buffer every time.
            free(buf);
        }
    }
    return 0;
}


