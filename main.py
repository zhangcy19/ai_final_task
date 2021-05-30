#main.py

#主逻辑

import sys
import interface
import sampleAI
import heuristicAI
import reinforcementAI

msg = "usage:  main.py [sample/heuristic/reinforcement] -off"
str = "*" * 30

if len(sys.argv) < 2 or len(sys.argv) >3:
    print(msg)
    exit(0)

api = interface.MyAPI()
with open("assist_data/state.txt", "r") as f:
    state = f.read()
    if state == "1":
        api.Image.loadArea()
        api.loadPath()                
    else:
        api.getPath()
        api.Image.getArea()
        api.Image.saveArea()
with open("assist_data/state.txt", "w") as f:
    f.write("1")

if len(sys.argv) == 3 and sys.argv[2] == "off":
    api.Assistant.visualize = "off"
elif len(sys.argv) == 2:
    api.Assistant.visualize = "image"
else:
    print(msg)
    exit(0)

if sys.argv[1] == "sample":
    print(str)
    print("\t启动样例AI")
    print(str)
    sampleAI.MyAI(api)
elif sys.argv[1] == "heuristic":
    print(str)
    print("\t启动启发式AI")
    print(str)
    heuristicAI.MyAI(api)
elif sys.argv[1] == "reinforcement":
    print(str)
    print("\t启动强化学习AI")
    print(str)
    reinforcementAI.MyAI(api)
else:
    print(msg)
    exit(0)
