CXX = cc
CFLAGS = -g -Wall 

all: testDevice myShell

.cc.o:
	$(CXX) -c $(CFLAGS) $<

clean:
	rm -f *.o *.dev

spotless: clean
	rm -f testDevice testBlockmap myShell

TEST_DEV_OBJS = block_device.o test_device.o master_block.o block_map.o 
SHELL_OBJS = my_shell.o block_device.o master_block.o block_map.o 

testDevice: $(TEST_DEV_OBJS)
	$(CXX) -o testDevice $(TEST_DEV_OBJS)

myShell: $(SHELL_OBJS)
	$(CXX) -o myShell -lreadline $(SHELL_OBJS)

test: all
	./testDevice
