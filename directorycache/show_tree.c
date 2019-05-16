
#include "filesystem.h"
#include "directory_cache.h"

int main(int argc, char **argv) {
    {
        FileSystem_t   fs2 = mount("dctest.dev");
        DirectoryEntry_t d = getChildren(fs2->root_dir, fs2);
        while (d != NULL) {
            printf("%s\t", d->name);
            d = d->next_sibling;
        }
        printf("\n");
        unmount(fs2);
    }
}
