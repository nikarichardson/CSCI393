File System Completion: Directory Cache Implementation  
By Nika R. 

To run, type make. Examine executables for ./testdirCache ./testParse and ./showTree. ./testParse shows the breakWords function in action, which parses directories. This code represents the final project of the file system implementation. 

A directory is a set of mappings of an inode number (low-level) and a name. We separate directory entries with a newline character '\n'. 
Individual entries contain a name with a pipe | and then the inode number. 

getChildren() manages the cache of directory entries and fetches children lazily (i.e. as needed). 

Some changes were made: "." now points to the directory inode as intended, sprintf() is used instead of more abstruse code involving indices. Finally, the code converting the inode num to a character—which only works on numbers 1-10—was removed in this process. 

In getChildren(), we preserve the i=0 case which is pulled out separately from the rest of the code because we need to assign the first child of 
the list to a DirectoryEntry called **prev**, which will be used within the loop as we extract the children Directory Entries. 