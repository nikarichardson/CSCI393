// Master Block

#include "block_device.h"
#include "master_block.h" //** 

#include <stdlib.h>
#include <unistd.h>
#include <errno.h>
#include <string.h>
#include <assert.h>
#include <stdbool.h>

#define MAGIC 0xFEEDC0DE
#define BLOCKSIZE 1024
#define BLOCKS_PER_DEVICE 100


// =============== =============== MASTER BLOCK: A P I =============== =============== 
// reads a MasterBlock from BlockDevice @ disk_location
// filling in the passed-in structure
// returns 0 on success, <0 on failure if the magic number doesn't match MAGIC_NUM 
// =============== =============== MasterBlock (Read) =============== =============== 
int readMasterBlock(BlockDevice *bd, MasterBlock *mb, disk_addr_t disk_location){ 
	int byteOffset = disk_location * bd->m_bytesPerBlock;
	int seekRet = lseek(bd->m_deviceHandle, disk_location*BLOCKSIZE, SEEK_SET);
	if (seekRet != byteOffset) {
		fprintf(stderr, "Seek error in readMasterBlock.\n");
		return -1;
	}
	// the disk address is the number of blocks between the start of the disk and the block 
	// formally was int numRead = but I got an unused variable warning
	read(bd->m_deviceHandle, mb, sizeof(struct MasterBlock)); 
	fprintf(stdout,"Just read:\n magic_num: %llx \n bytes_per_block : %u \n blocks_per_device:  %d \n disk address: %d \n",
		 mb->magic_num, mb->bytes_per_block, mb->blocks_per_device, mb->disk_addr_of_block_map);
	if (mb->magic_num == MAGIC){
		//fprintf(stdout, "YAYAYAYAYAYAYAYAY MAGIC NUM IS RIGHT! KEEP FEEDING ME CODE!!\n");
		return 0;
	} else {
		fprintf(stderr, "Magic number is not right. Illegit file system!\n");
		return -1; 
	}
 
}

// writes MasterBlock pointed to by mb to the block device @ disk_location
// returns 0 on success, <0 if the write fails
// if there are n blocks (numbers of blocks)
// then the address space is numbered from 0 to n-1 
// should write a MasterBlock pointed to by Masterblock pointer 
// =============== =============== MasterBlock (Write) =============== =============== 
int writeMasterBlock(BlockDevice *bd, MasterBlock* mb, disk_addr_t disk_location){
	int seekRet = lseek(bd->m_deviceHandle,disk_location*BLOCKSIZE,SEEK_SET);
	int byteOffset = disk_location * bd->m_bytesPerBlock;
	if (seekRet != byteOffset) {
		fprintf(stderr, "Seek error in writeMasterBlock.\n");
		return -1;
	} 
	// writes data pointed to by mb to the block device at disk_location
	int numWritten = write(bd->m_deviceHandle, (struct MasterBlock*) mb, sizeof(struct MasterBlock));

	if (numWritten != sizeof(struct MasterBlock)) {
		fprintf(stderr, "Write error in writeMasterBlock.\n");
		return -1;
	}
	return 0; 
}

// helper function 1: allocate memory for a Master Block and initilize its fields
// with the parameters to this function
// =============== =============== MasterBlock (Allocate) =============== =============== 
master_block_t allocMasterBlock (int b_per_block, int number_of_b, disk_addr_t b_map_address){
	master_block_t mb = malloc(sizeof(MasterBlock));
	mb->magic_num = MAGIC; 
	mb->bytes_per_block = b_per_block; 
	mb->blocks_per_device = number_of_b; 
	mb->disk_addr_of_block_map = b_map_address;  
	return mb;  

}

// helper function 2: free memory allocated in allocateMasterBlock
// =============== =============== MasterBlock (Free) =============== =============== 
void freeMasterBlock(master_block_t mb){
	free(mb); // statement frees the space allocated in the memory pointed by mb
}

// Block Device is opened, but the parameters are not initialized! Yikes.
// We can fix that by being clever. 
int bootstrapDeviceFromMasterBlock(BlockDevice *bd){ 
	char* buf = malloc(sizeof(MasterBlock)); // size of MasterBlock 
	if (read(bd->m_deviceHandle,buf,sizeof(MasterBlock))> 0){
		// char temp[15];
		// sprintf(temp, "%u", MAGIC); 
		// int offset1 = strlen(temp); // magic number
		// int blockCount = atoi(buf + offset);
		master_block_t mbp = (MasterBlock*)buf; 
		int bytesPerBlock = mbp->bytes_per_block; 
		int blockCount = mbp->blocks_per_device; 
		setupBlockDevice(bd, blockCount, bytesPerBlock); 
		return 1; // successfully bootstrapped device from masterblock  
	} else {
		return -1; 
	}
}