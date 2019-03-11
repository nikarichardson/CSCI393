#include "block_device.h"
#include "block_device.c"
#include <readline/readline.h>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/wait.h>
#include <readline/history.h>
#define ARR_BUFF 64
#define DELIM " \t\r\n\a"
#define BUFFER_SIZE 1024


char **split(char *line)
{
  // This code is adapted from shell code available online that splits the arguments 
  // into an array. I'm not sure if we were supposed to build this function separately,
  // or if there is some built-in C function/library that can do this work. 
  // I know Python has sys.argv . . . 
  int bufsize = BUFFER_SIZE, position = 0;
  char **args = malloc(bufsize * sizeof(char*));
  char *arg;

  arg = strtok(line, DELIM);
  while (arg != NULL) {
    args[position] = arg;
    position++;

    if (position >= bufsize) {
      bufsize += ARR_BUFF;
      args = realloc(args, bufsize * sizeof(char*));
    }
    arg = strtok(NULL, DELIM);
  }
  args[position] = NULL;
  return args;
}


int main(int argc, char** argv) {
  printf("Welcome! You can exit by pressing Ctrl+C at any time...\n");

  rl_bind_key('\t', rl_insert);

  char* buf;
  char **args;
  // We maintain a device_t object that should probably be globally stored. 
  // Then we allocate space for a devices_t object, which is essentially
  // a linkedlist of BlockDevices. 
  devices_t * d = NULL; // HMM SHOULD BE GLOBAL 
  d = malloc(sizeof(devices_t));
  d->dev = NULL; 
  d->next = NULL; 
  devices_t * curr = d;

  while ((buf = readline(">> ")) != NULL) {
    args = split(buf);

    // =================================================
    // newfs := creates new BlockDevice, new MasterBlock & new BlockMap
    // =================================================
    // newfs <block_device_name> <bytes_per_block> <block_count> 
    // ex. newfs myFS.dev 1024 10
    if (strcmp("newfs",args[0]) == 0){
      // Create new BlockDevice
      int block_size =  atoi(args[2]);
      int block_count = atoi(args[3]);
      block_device_t t = createBlockDevice(args[1], block_size, block_count);
      // Create new MasterBlock
      int addr = 0;
      master_block_t m = allocMasterBlock(block_size,block_count,addr,t);
      writeMasterBlock(t, m, addr);
      
      // Create new Blockmap 
      BlockMap_p bm = createBlockMap(block_count); 
      addr += 1; 
      writeBlockMap(bm,t,addr); 

      printf("%s created with %d blocks of %d bytes each\n",args[1],block_count,block_size);
      curr = d; 
      // Iterate to the end of the list 
      if (curr->dev == NULL){
        curr = malloc(sizeof(devices_t));
        curr->dev = t; 
      } else {
          while (curr->next != NULL) {
            curr = curr->next;
          } 
          // Add this device to the linked list of devices. 
          curr->next = malloc(sizeof(devices_t)); 
          curr->next->dev = t; 
          curr->next->next = NULL; 
      }
    }

    // =================================================
    // Mount := mounts new file system 
    // =================================================
    // mount <block_device_name>
    if (strcmp("mount",args[0]) == 0){
      while (1){
        if (strcmp(curr->dev->deviceName,args[1]) == 0){
          break; 
        } else {
          curr = curr->next; 
        }
      }
      // Now curr should be equal to the current file system. 
      printf("%s mounted\n",args[1]);
    }

    // =================================================
    // allocBlock := allocates a block & prints the number of the block allocated
    // =================================================
    if (strcmp("allocBlock",args[0]) == 0){
      printf("allocBlock");
    }

    // =================================================
    // freeBlock <n> := frees block n
    // =================================================
    if (strcmp("freeBlock",args[0]) == 0){
      printf("freeBlock");
    }

    // =================================================
    // blockMap := prints the blockmap
    // =================================================
    if (strcmp("blockMap",args[0]) == 0){
      printf("block count of device %d\n",curr->dev->m_blockCount);
      BlockMap_p b = allocBlockMap(10); 
      readBlockMap(b,curr->dev,1);
      printBlockMap(b); 
    }

    // =================================================
    // unmount := writes the Block Map back to the block device
    // =================================================
    if (strcmp("unmount",args[0]) == 0){
      while (1){
        if (strcmp(curr->dev->deviceName,args[1]) == 0){
          break; 
        } else {
          curr = curr->next; 
        }
      }
      // writeBlockMap(BlockMap *b,curr->dev,1)

      printf("%s un-mounted.\n",args[1]);
    }
    free(buf);
    free(args);
  }

  return 0;
}

