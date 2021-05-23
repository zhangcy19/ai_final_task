#main.py

#主逻辑

import sys
import interface
import sampleAI
import heuristicAI
import reinforcementAI

api = interface.MyAPI()
msg = "usage:  main.py [init/uninit] [off/image/video] [sample/heuristic/reinforcement]"
str = "*" * 30

if len(sys.argv) != 4:
    print(msg)

if sys.argv[1] == "init":
    api.Image.getArea()
    api.Image.saveArea()
elif sys.argv[1] == "uninit":
    api.Image.loadArea()
else:
    print(msg)

if sys.argv[2] in ["off", "image", "video"]:
    api.Assistant.visualize = sys.argv[2]
else:
    print(msg)

if sys.argv[3] == "sample":
    print(str)
    print("\t启动样例AI!")
    print(str)
    sampleAI.MyAI(api)
elif sys.argv[3] == "heuristic":
    print(str)
    print("\t启动启发式AI!")
    print(str)
    heuristicAI.MyAI(api)
elif sys.argv[3] == "reinforcement":
    print(str)
    print("\t启动强化学习AI!")
    print(str)
    reinforcementAI.MyAI(api)
else:
    print(msg)
