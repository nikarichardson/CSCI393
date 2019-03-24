print("newfs everest_small.dev 256 100");
print("mount everest_small.dev"); 
print("allocateINode");  
print("allocateINode"); 
print("getStatus 1") ## 
print("getStatus 2") ## 
print("getStatus 3");  
print("allocateINode"); 
print("freeINode 3");
print("getStatus 3"); 
print("freeINode 3");
print("unmount"); 
print("mount everest_small.dev"); 
print("getStatus 1") ## 
print("getStatus 2") ## 
print("getStatus 3");  
print("allocateINode"); 
for i in range(30):
    print("allocateINode");
print("unmount"); 
print("mount everest_small.dev"); 
for i in range(3,15):
    print("getStatus ",i);
for i in range(3,15):
    print("freeINode ",i);
for i in range(3,15):
    print("getStatus ",i);
print("q");