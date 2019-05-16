#include "filesystem.h"
#include "directory_cache.h"

char *testDir1 = "hello|10\nthere|42\nworld|43\n";

int main(int argc, char **argv) {
    char *in = 1 + malloc(strlen(testDir1));
    strcpy(in, testDir1);
    printf("parsing %s", in);
    // a directory has a number of lines, separated by \n, so the
    // number of \n's is the number of children
    int numDirEntries = countOccurrences(in, '\n', strlen(in));
    char **lines = calloc(numDirEntries, sizeof(char *));
    int check = breakWords(in, lines, numDirEntries, "\n");
    assert(check == numDirEntries);
    for (int i = 0; i < numDirEntries; i++) {
        // each row / entry is a name|inode_number pair, so now split
        // it by | to get the two components:
        char **words = calloc(2, sizeof(char *));
        int shouldBeTwo = breakWords(lines[i], words, 2, "|");
        assert(shouldBeTwo == 2 && "uh oh, not exactly one | in a dir entry");
        int inode_num = atoi(words[1]);
        printf("got a directory: %s -> inode %d\n", words[0], inode_num);
    }
}
