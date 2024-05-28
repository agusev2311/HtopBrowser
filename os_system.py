import os
# a = os.system("ps")
a = os.popen("ps", mode='r', buffering=-1)
b = a.read()
for i in range(5):
    print(b)