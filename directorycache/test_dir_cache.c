
#include "filesystem.h"
#include "directory_cache.h"

int main(int argc, char **argv) {
    {
        printf("----------- Test 1 ----------- \n"); 
        newfs("dctest.dev", 1024, 100, 16);
        FileSystem_t   fs = mount("dctest.dev");
        INodeAddr_t i_num = allocateINode(fs);
        INode_t     inode = getINode(fs, i_num);
        addChild(fs->root_dir, "foo", inode); 
        // unmount will call flushDirectoryCache 
        unmount(fs);
        printf("\n"); 
    } 


    {
        printf("----------- Test 2 ----------- \n"); 
        FileSystem_t   fs2 = mount("dctest.dev");
        // getChildren() 
        printf("                 getChildren of "); 
        printf("%s:",fs2->root_dir->name); 
        DirectoryEntry_t d = getChildren(fs2->root_dir, fs2); 
        while (d != NULL) {
            printf("\tCHILD %s\t", d->name);
            d = d->next_sibling;
        }

        // create child bar 
        INodeAddr_t i_num = allocateINode(fs2);
        INode_t     inode = getINode(fs2, i_num);
        addChild(fs2->root_dir, "bar", inode);
        // create child totem
        INodeAddr_t i_num2 = allocateINode(fs2);
        INode_t     inode2 = getINode(fs2, i_num2);
        addChild(fs2->root_dir, "totem", inode2);
        
        // getChildren() 
        printf("                 getChildren of "); 
        printf("%s:",fs2->root_dir->name); 
        d = getChildren(fs2->root_dir, fs2); 
        while (d != NULL) {
            printf("\tCHILD %s\t", d->name);
            d = d->next_sibling;
        }
        printf("\n");
        unmount(fs2); 
    } 
   
   {
        printf("----------- Test 3 ----------- \n"); 
        FileSystem_t   fs3 = mount("dctest.dev");
        printf("                 getChildren of "); 
        printf("%s:",fs3->root_dir->name); 
        DirectoryEntry_t d = getChildren(fs3->root_dir, fs3); 
        while (d != NULL) {
            printf("\tCHILD %s\t", d->name);
            d = d->next_sibling;
        }
        printf("\n");


        printf("                 getChildren of "); 
        printf("%s:",fs3->root_dir->maybe_children->name); 
        d = getChildren(fs3->root_dir->maybe_children, fs3); 
        while (d != NULL) {
            printf("\tCHILD %s\t", d->name);
            d = d->next_sibling;
        }
        printf("\n");


        unmount(fs3);
    }   
}
