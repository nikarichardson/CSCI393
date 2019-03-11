// Operating Systems 
// Test Device, Modified from Dylan Test Device

#include "block_device.h"
#include "block_map.h"
#include "master_block.h"
#define BLOCKSIZE 1024

int main() {
	// Test block device. 
	char buf[BLOCKSIZE] = " Shiny new block device!";
	char readBuf[BLOCKSIZE];
	block_device_t t = createBlockDevice("foo.dev", BLOCKSIZE, 100); // 100 is our block count 
	for (int j = 0; j < 10; j++) {
		buf[j] = '0' + j;
		writeBlock(t, j, buf);
		memset(readBuf, 0, BLOCKSIZE);
		readBlock(t, j, readBuf,t->m_bytesPerBlock);
		for (int i = 0; i < BLOCKSIZE; i++){
			if (buf[i] != readBuf[i]) {
				printf("Buffer Mismatch\n");
			}
		}
	}
	printf( "All block device tests are complete.\n");
	// Create a master block. 
	int BYTES_PER_BLOCK = BLOCKSIZE; // has to match the bytes per block of the block device  
	int addr = 0;
	master_block_t m = allocMasterBlock(BYTES_PER_BLOCK,BLOCKS_PER_DEVICE,addr);
	printf("magic_num: %llx",m->magic_num); 
	printf("\n compare with: %x \n",0xFEEDC0DE); 
	printf("bytes_per_block : %u",m->bytes_per_block); 
	printf("\n compare with: %u\n",BYTES_PER_BLOCK); 
	printf("blocks_per_device: %d",m->blocks_per_device);
	printf("\n compare with: %u\n",100);  
	printf("disk_addr_of_block_map: %d",m->disk_addr_of_block_map); 
	printf("\n compare with: %d\n",addr); 
	writeMasterBlock(t, m, addr);
	readMasterBlock(t,m,addr);

	// Test read master block function. 
	freeMasterBlock(m);
	printf( "Master block device tests complete.\n");
	addr += 1; 

	// Test block map 
	BlockMap_p bm = allocBlockMap(10);  
	printf("blockmap1: ");
	printBlockMap(bm); 
	printf("allocItem: "); 
	printf("%d\n",allocItem(bm));
	printf("allocItem: "); 
	printf("%d\n",allocItem(bm));
	printf("allocItem: "); 
	printf("%d\n",allocItem(bm));
	printf("blockmap1: ");
	printBlockMap(bm); 
	// Now write it to the address
	BlockMap_p bm2 = allocBlockMap(10); 
	printf("blockmap2: ");
	printBlockMap(bm2); 
	closeBlockDevice(t); 
}
