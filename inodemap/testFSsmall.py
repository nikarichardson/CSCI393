print("newfs testpy.dev 256 100");
print("mount testpy.dev");
print("blockMap");
for i in range(50):
    print("allocBlock");
print("blockMap");
for i in range(25):
    print("freeBlock ", 2*i);
print("unmount");
print("mount testpy.dev");
print("blockMap");
print("allocBlock");
print("allocBlock");
print("allocBlock");
print("unmount");

