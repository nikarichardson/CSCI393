print("newfs testgo.dev 1024 100");
print("mount testgo.dev"); 
print("blockMap");
for i in range(2,88):
    print("allocBlock");
print("blockMap"); 
for i in range(2,44): 
    print("freeBlock ", 2*i);
print("blockMap"); 
print("unmount");  
print("mount testgo.dev");  
print("blockMap"); 
print("allocBlock");
print("allocBlock");
print("allocBlock");
print("q");



