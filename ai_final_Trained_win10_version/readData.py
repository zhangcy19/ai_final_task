import sys
import os

score = 0
with open("assist_data\score.txt", "r") as f:
    score = int(f.read())

current_path = str(sys.argv[1])
current_path = current_path[:len(current_path)-7]
for root,dirs,files in os.walk(current_path):
    for name in files:
        if not str(os.path.join(root,name)).endswith('json'):
            continue
        with open(os.path.join(root,name),'r',encoding='UTF-8',errors='ignore') as f:
            temp = f.read()
            temp = int(str(temp).strip(u'\ufeff'))
        if temp > score:
            with open("assist_data\score.txt", "w") as f:
                f.write(str(temp))
        os.remove(os.path.join(root,name))
