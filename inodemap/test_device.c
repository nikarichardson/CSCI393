#include "block_device.h"

#define BLOCKSIZE 1024
int main() {
    char buf[BLOCKSIZE] = " hello there shiny block device";
    char readBuf[BLOCKSIZE];
    block_device_t bd = createBlockDevice("foo.dev", BLOCKSIZE, 100);
    for (int j = 0; j < 10; j++) {
        buf[j] = '0' + j;
        writeBlock(bd, j, buf);
        memset(readBuf, 0, BLOCKSIZE);
        readBlock(bd, j, readBuf);
        for (int i = 0; i < BLOCKSIZE; i++){
            if (buf[i] != readBuf[i]) {
                printf( "buffer mismatch\n");
            }
        }
    }
    closeBlockDevice(bd);
    printf( "device tests complete\n");
}
