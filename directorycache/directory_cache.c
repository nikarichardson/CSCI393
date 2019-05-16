#include "directory_cache.h"
#include <assert.h>
#include <string.h>
#include <stdlib.h>
#include <string.h>
#include <stdio.h>

// allocates a DirectoryEntry for this name->inode mapping 
// and adds it to the parent's linked list of maybe_children
void addChild(DirectoryEntry_t parent, char *name, INode_t inode){
  

    // create a new Directory Entry    
    struct DirectoryEntry *d; 
    d = malloc(sizeof(struct DirectoryEntry)); 
    // no other children yet 
    d->inode_ptr = inode; 
    d->name = name; 
    // a new child has NULL maybe_children directories  
    d->maybe_children = NULL;
    d->is_dirty = false; 
    // we add this child to the children list of parent
    d->next_sibling = parent->maybe_children;
    parent->maybe_children = d; // set children of parent root equal to bar
    // parent directory is uncached once we add children 
    parent->is_dirty = true; 
    printf("\n                                                                                                            [child %s created with parent %s]\n",parent->maybe_children->name,parent->name);
}

// creates the root directory entry 
void addRoot(FileSystem_t fs, INode_t inode){
    struct DirectoryEntry *d; 
    d = malloc(sizeof(struct DirectoryEntry)); 
    d->inode_ptr = inode; 
    d->name = "root";  
    d->next_sibling = NULL; 
    d->maybe_children = NULL;
    d->is_dirty = true;
    // set the filesystem's root directory to be newly created directory entry 
    fs->root_dir = d;  
}


// returns the linked list of children in a directory 
// note: each directory entry owns the memory pointed to by its name entry
// & each directory owns the linkedlist which constitute its 'maybe_children' 
DirectoryEntry_t getChildren(DirectoryEntry_t dir, FileSystem_t fs) {
    assert(dir && "getChildren dir == null");
    assert(dir->inode_ptr && "getChildren, inode_ptr == null");

    // if directory is cached (written to disk) we return its children 
    if (dir->maybe_children != NULL) { 
        return dir->maybe_children; 
    } 

    // the only time dir->maybe_children is NULL is when a directory is uncached 
    // if our directory is_dirty, (that is, uncached) 
    // we read directory contents from the inodes
    int num_bytes = dir->inode_ptr->num_bytes;  
    if (num_bytes == 0){
        // if directory is uncached & has no children, we include
        // a directory entry for "." which points to its own inode
        struct DirectoryEntry *h; 
        h = malloc(sizeof(struct DirectoryEntry)); 
        h->name = ".";  
        h->maybe_children = NULL;
        h->is_dirty = false; 
        h->inode_ptr = dir->inode_ptr;  
        h->next_sibling = NULL; 
        dir->maybe_children = h; 
        return dir->maybe_children; 
    } 
    
    char *in_buffer = malloc(num_bytes);
    int bytes_in_dir = num_bytes; 
    int start = 0;  

    // we read from the inode for this directory entry into buffer named in_buffer  
    int bytes_read = iNodeRead(dir->inode_ptr,start,bytes_in_dir,in_buffer,fs); 
    if (bytes_read != num_bytes) {
        fprintf(stderr,"error in bytes read from INodeRead in getChildren");
    } 

    // gets number of children by passing in_buffer with contents from iNodeRead
    int num_children = countOccurrences(in_buffer,'\n',num_bytes);  
    char **out_buffer = malloc(num_children * sizeof(char *));

    // applies the breakWords parsing function to the content 
    int j = breakWords(in_buffer,out_buffer,num_children,"\n");
    if (j != num_children){
        fprintf(stderr,"error in num_children read from parsing\n");
    }

    // we pull out the i=0 case here 
    // so that we can assign prev to the first entry 
    // which we will use inside the loop 
    // head of list, i.e. first child
    char *pair[2];
    char *name = malloc(MAX_DIR_NAME_LEN); 
    // apply breakWords again to separate the name from inode num 
    breakWords(out_buffer[0],pair,2,"|");
    strcpy(name, pair[0]);
    int inode_num = atoi(pair[1]); 
    struct DirectoryEntry *prev; 
    prev = malloc(sizeof(struct DirectoryEntry));
    prev->name = name;
    prev->inode_ptr = &fs->inode_map[inode_num];  
    prev->maybe_children = NULL;
    prev->is_dirty = false; 
    dir->maybe_children = prev; 
    dir->is_dirty = true;

    for (int i = 1; i < j; i++){
        char *pair2[2];
        char *name2 = malloc(MAX_DIR_NAME_LEN); 
        // apply breakWords again to separate the name from inode num 
        breakWords(out_buffer[i],pair2,2,"|");
        strcpy(name2, pair2[0]);
        int inode_num2 = atoi(pair[1]); 
        struct DirectoryEntry *d; 
        d = malloc(sizeof(struct DirectoryEntry)); 
        d->name = name2;
        d->is_dirty = true; 
        d->inode_ptr = &fs->inode_map[inode_num2];  
        d->maybe_children = NULL;
        // previous of old sibling equals this new directory entry 
        prev->next_sibling = d; 
        // now new directory entry becomes the new previous 
        prev = d; 
    }
    return dir->maybe_children; 
}


// writes a directory to its inode: a directory is
// a linearization of the contents of a directory, 
// a set of mappings from name to inode-number 
void writeDirectory(DirectoryEntry_t d, FileSystem_t fs) {
    char buf[MAX_DIR_ENTRY_LEN];
    int start = 0; 
    // create a temporary directory entry for looping purposes
    DirectoryEntry_t temp = d; 
    if (temp->maybe_children != NULL){
        // get the first child
        temp = temp->maybe_children; 
        sprintf(buf, "%s|%d\n", temp->name, temp->inode_ptr->inode_num); 

        // now add the other children by looping through next_sibling 
        while (temp->next_sibling != NULL){
            temp = temp->next_sibling; 
            sprintf(buf + strlen(buf), "%s|%d\n", temp->name, temp->inode_ptr->inode_num);
        }
    }


    // write the buf into the inode
    int num_bytes_to_write = sizeof(buf); 
    int bytes_written = iNodeWrite(d->inode_ptr,start,num_bytes_to_write,buf,fs); 
    if (bytes_written != num_bytes_to_write){
        fprintf(stderr,"num bytes written in writeDirectory not correct\n"); 
    }

    // mark directory as clean now that it has been written to disk
    d->is_dirty = true; 
}

// recursively writes all of the dirty directory entries back to disk 
void flushDirectoryCache(DirectoryEntry_t dir, FileSystem_t fs) {
    // if directory is uncached 
    if (dir->is_dirty == true) {    
        writeDirectory(dir,fs);
    } 

    // recursive calls 
    if (dir->maybe_children != NULL){
        dir = dir->maybe_children; 
        flushDirectoryCache(dir,fs); 
    } 

    if (dir->next_sibling != NULL){
        dir = dir->next_sibling; 
        flushDirectoryCache(dir,fs); 
    }
} 


// helper function for getChildren
int countOccurrences(char *buf, char c, int bsize){
    int ret = 0;
    for (int i = 0; i < bsize; i++) {
        if (buf[i] == c) ret++;
    }
    return ret;
}
