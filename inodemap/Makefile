# CXX = gcc-8
CXX = cc
CFLAGS = -g -O0 -Wall

all: myShell mytests 

edit:
	vim my_shell.c filesystem.c master_block.c master_block.h dylan_bit_set.c dylan_bit_set.h block_device.h block_device.c inode.h inode.c 

mytests: mygoodoutput.log inode_output.log inodesmall_output.log
	python3 mytestFS.py | ./myShell | diff mygoodoutput.log -
	python3 inodetest.py | ./myShell | diff inode_output.log - 
	python3 testFSsmall.py | ./myShell | diff mysmalloutput.log -  
	python3 inodetestsmall.py | ./myShell | diff inodesmall_output.log - 

mysmalloutput.log:
	python3 testFSsmall.py | ./myShell > mysmalloutput.log 

mygoodoutput.log:
	python3 mytestFS.py | ./myShell > mygoodoutput.log

inode_output.log: 
	python3 inodetest.py | ./myShell > inode_output.log

inodesmall_output.log: 
	python3 inodetestsmall.py | ./myShell > inodesmall_output.log

.cc.o:
	$(CXX) -c $(CFLAGS) $<

clean:
	rm -f *.o *.dev

spotless: clean
	rm -f testDevice testBlockmap myShell *.log

TEST_DEV_OBJS = block_device.o test_device.o master_block.o dylan_bit_set.o inode.o 
SHELL_OBJS = my_shell.o block_device.o master_block.o dylan_bit_set.o inode.o filesystem.o

testDevice: $(TEST_DEV_OBJS)
	$(CXX) -o testDevice $(TEST_DEV_OBJS)

myShell: $(SHELL_OBJS)
	$(CXX) -o myShell $(SHELL_OBJS) -lreadline

RELEASE_FILES = Makefile Readme.txt block_device.c block_device.h dylan_bit_set.c dylan_bit_set.h inode.c inode.h filesystem.c filesystem.h master_block.c master_block.h my_shell.c testFS.py testFSsmall.py test_device.c

tarball: $(RELEASE_FILES)
	tar czf release.tgz $(RELEASE_FILES)
