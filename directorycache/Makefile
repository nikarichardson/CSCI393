# CXX = gcc-8
CXX = cc
CFLAGS = -g -O0 -Wall

all: myShell tests testDirCache showTree testParse

tests: goodoutputsmall.log
	python3 testFSsmall.py | ./myShell | diff goodoutputsmall.log -

goodoutputsmall.log:
	python3 testFSsmall.py | ./myShell > goodoutputsmall.log

edit:
	vim inode.c inode.h my_shell.c filesystem.c master_block.c master_block.h dylan_bit_set.c dylan_bit_set.h block_device.h block_device.c

.cc.o:
	$(CXX) -c $(CFLAGS) $<

clean:
	rm -f *.o *.dev

spotless: clean
	rm -f testDevice testBlockmap myShell *.log testDirCache showTree testParse newShell

TEST_DEV_OBJS = block_device.o test_device.o master_block.o dylan_bit_set.o
FS_OBJS = block_device.o master_block.o dylan_bit_set.o filesystem.o inode.o directory_cache.o
SHELL_OBJS = my_shell.o $(FS_OBJS)
NEW_SHELL_OBJS = new_shell.o $(FS_OBJS)
TEST_DIR_CACHE_OBJS = test_dir_cache.o $(FS_OBJS)
SHOW_TREE_OBJS = show_tree.o $(FS_OBJS)
TEST_PARSE_OBJS = test_parse.o $(FS_OBJS)

testDevice: $(TEST_DEV_OBJS)
	$(CXX) -o testDevice $(TEST_DEV_OBJS)

newShell: $(NEW_SHELL_OBJS)
	$(CXX) -o newShell $(NEW_SHELL_OBJS) -lreadline

myShell: $(SHELL_OBJS)
	$(CXX) -o myShell $(SHELL_OBJS) -lreadline

testDirCache: $(TEST_DIR_CACHE_OBJS)
	$(CXX) -o testDirCache $(TEST_DIR_CACHE_OBJS)

showTree: $(SHOW_TREE_OBJS)
	$(CXX) -o showTree $(SHOW_TREE_OBJS)

testParse: $(TEST_PARSE_OBJS)
	$(CXX) -o testParse $(TEST_PARSE_OBJS)
