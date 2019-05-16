""" basic smoke test
    tests a 1-block blockmap
    creates a file system
    mounts it
    allocates stuff
    frees every other one
    unmounts
"""

print("newfs testpy.dev 256 100");
print("mount testpy.dev");
for i in range(100):
    print("allocBlock");
print("blockMap");
for i in range(50):
    print("freeBlock ", 2*i);
print("allocINode");
print("allocINode");
print("unmount");
