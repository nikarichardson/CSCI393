#include "block_device.h"
#include "master_block.h"
#include "dylan_bit_set.h"
#include "inode.h"
#include "filesystem.h"

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

// C doesn't have C++ (or Python)'s handy "split" function.
// breakWords takes an input string and an array of pointers to strings.
// It sets each element of the array to the next word, and returns the
// total number of words parsed. max_words is the length of the array
// of pointers.
int breakWords(char *in, char **out, int max_words) {
    const char *delim = " \t"; // separating tokens
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
            // the next token, which we hope is the filename this time
            words = strtok(NULL, delim);
        } else {
            // we're setting out[i] to NULL, which is good
        }
    }
    return j;
}

void unmount(block_device_t bd, master_block_t mb, BlockMap_t bs,INode *inode_map, int num_inodes) {
    // write the block map to disk
    int writeZero = writeBlockMap(bd, bs, 1);

    // write inode map to disk 
    int writeTwoZero = writeINodeMap(bd, inode_map, 2, num_inodes);

    // close the file
    int closeZero = closeBlockDevice(bd);

    // set the mb to NULL
    if (writeZero == 0 && closeZero == 0 && writeTwoZero == 0) {
        printf("unmount successful\n");
    } else {
        fprintf(stderr, "unmount error\n");
    }
}

int main(int argc, char** argv) {
    printf("Welcome! You can exit by pressing Ctrl+C at any time...\n");

    bool done = false;
    char* buf;
    master_block_t main_mb = NULL; // the master block
    block_device_t main_bd = NULL; // the block device
    BlockMap_t       main_bs = NULL; // the blockmap (a bitset)
    INode *main_im = NULL; // the inode map 

    const int MAX_ARGS = 32;
    char *arguments[MAX_ARGS];
    int num_inodes = 100; 

    while (!done && (buf = readline(">> ")) != NULL) {
        if (strlen(buf) == 0) {
            continue; // user pressed enter
        }
        add_history(buf);

        int num_words = breakWords(buf, arguments, MAX_ARGS);
        if (equals("q", arguments[0], false)) {
            if (main_bd != NULL) {
                unmount(main_bd, main_mb, main_bs,main_im,num_inodes);
            }
            done = true;
        } else if (equals("newfs", arguments[0], true)) {
            if (num_words == 4) {
                char *device_name = arguments[1];
                // atoi is ASCII -> integer, so get the block size
                // into an integer.
                int block_size = atoi(arguments[2]);
                // and now read the number of blocks
                int block_count = atoi(arguments[3]);
                // now we know everything we need to create
                // the device.
                int newfs_ok = newfs(device_name, block_size, block_count);
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
                main_bd = bootstrapDevice(device_name);
                if (main_bd != NULL) {
                    // main_bd now points to a working, initialized block device
                    const int mb_loc = 0;
                    const int bm_loc = 1;
                    const int im_loc = 2; 
                    if ( (main_mb = readMasterBlock(main_bd, mb_loc)) != NULL && 
                        (main_bs = readBlockMap(main_bd, bm_loc)) != NULL && 
                        (main_im = readINodeMap(main_bd,main_im,im_loc,num_inodes)) != NULL ) {
                        printf("successfully mounted %s \n", device_name);
                    } else {
                        fprintf(stderr, "mount failed.\n");
                        main_bd = NULL;
                        main_mb = NULL;
                        main_bs = NULL;
                        main_im = NULL; 
                    }
                } else {
                    fprintf(stderr, "open device failed. did you use the right filename?\n");
                    main_bd = NULL;
                }
            } else {
                fprintf(stderr, "usage: mount <device file name>\n");
            }
        } else if (equals("unmount", arguments[0], true)) {
            if (main_bd != NULL) {
                unmount(main_bd, main_mb, main_bs,main_im,num_inodes);
            } else {
                fprintf(stderr, "you need to mount before unmounting\n");
            }
        } else if (equals("allocBlock", arguments[0], true)) {
            if (main_bs != NULL) {
                int ba = allocItem(main_bs);
                if (ba >= 0) {
                    printf("    allocated %d\n", ba);
                } else {
                    printf("    unable to allocate block\n");
                }
            } else {
                fprintf(stderr, "you need to mount a filesystem first\n");
            }
        } else if (equals("freeBlock", arguments[0], true)) {
            char *btf_char = arguments[1];
            if (num_words == 2) {
                if (main_bs != NULL) {
                    int block_to_free = atoi(btf_char);
                    freeItem(main_bs, block_to_free);
                } else {
                    fprintf(stderr, "you need to mount a filesystem first\n");
                }
            } else {
                fprintf(stderr, "usage: freeBlock <blocknum>");
            }
        } else if (equals("blockMap", arguments[0], true)) {
            if (main_bs != NULL) {
                printf("%d blocks in Block Map\n", main_bs->count);
                for (int i = 0; i < main_bs->count; i++) {
                    putchar(getBit(main_bs, i) ? '1' : '0');
                }
                printf("\n");
            } else {
                fprintf(stderr, "you need to mount a filesystem first\n");
            }
        } else if (equals("echo", arguments[0], true)) {
            for (int i = 0; i < num_words; i++) {
                printf("%s ", arguments[i]);
            }
            printf("\n");
        }
        // allocate iNode
        else if (equals("allocateINode", arguments[0], true)) {
            if (main_im != NULL && main_bs != NULL && main_bd != NULL) {
                inode_addr_t allocated = allocateINode(main_im);
                fprintf(stdout,"    allocated INode @ address %d \n",allocated);
            } else {
                fprintf(stderr, "you need to mount a filesystem first\n");
            }
        }

        // getStatus iNode
        else if (equals("getStatus", arguments[0], true)) {
            char *btf_char3 = arguments[1];
            if (num_words == 2) {
                if (main_im != NULL) {
                    int block_to_free = atoi(btf_char3);
                    fprintf(stdout,"inode_map[%d] has status %d \n",block_to_free,getStatus(block_to_free,main_im));
                } else {
                    fprintf(stderr, "you need to mount a filesystem first\n");
                }
            } else {
                fprintf(stderr, "usage: getStatus <iNodenum>");
            }
        }

        // free iNode
        else if (equals("freeINode", arguments[0], true)) {
            char *btf_char2 = arguments[1];
            if (num_words == 2) {
                if (main_im != NULL) {
                    int block_to_free = atoi(btf_char2);
                    // int c = freeINode(block_to_free,main_im);
                    if (freeINode(block_to_free,main_im) == 0){
                        fprintf(stdout,"    freed INode @ address %d\n",block_to_free); 
                    } else { 
                        fprintf(stdout,"    inode @ address %d is already free.\n",block_to_free);
                    }
                    
                } else {
                    fprintf(stderr, "you need to mount a filesystem first\n");
                }
            } else {
                fprintf(stderr, "usage: freeINode <iNodenum>");
            }
        }

        // readline malloc's a new buffer every time.
        free(buf);
    }

    return 0;
}


