import json
import numpy as np
import torch
import torch.nn as nn
from collections import namedtuple

Transition = namedtuple("Transition", field_names=[
    "state", "action", "reward", "next_state", "done"])


class Test:
    def __init__(self):
        self.memory = []

    def load(self):
        """json读取"""
        with open("assist_data/Q_memory.json", "r") as f:
            dic = json.loads(f.read())
            dic = eval(dic)
            tdic = {}
            maxn = 0
            for ni, dic2 in dic.items():
                i = int(ni)
                maxn = max(maxn, i)
                dic2 = eval(dic2)
                tmpdic = {}
                for ni2, v2 in dic2.items():
                    i2 = int(ni2)
                    if i2 == 0 or i2 == 3:
                        v2 = eval(v2)
                        v2 = self.build(v2)
                    elif i2 == 1:
                        v2 = int(v2)
                    elif i2 == 2:
                        v2 = float(v2)
                    elif i2 == 4:
                        v2 = bool(v2)
                    tmpdic[i2] = v2
                tdic[i] = Transition(tmpdic[0], tmpdic[1], tmpdic[2], tmpdic[3], tmpdic[4])
            self.memory = []
            for i in range(maxn + 1):
                if i in tdic and tdic[i] is not None:
                    self.memory.append(tdic[i])
            print("已成功加载记忆数量:", maxn + 1)

    def save(self):
        """json存储"""
        with open("assist_data/Q_memory.json", "w") as f:
            dic = {}
            for i, v in enumerate(self.memory):
                if v is None:
                    continue
                dic2 = {}
                for i2, v2 in enumerate(v):
                    if i2 == 0 or i2 == 3:
                        v2 = self.plain(v2)
                    v2 = json.dumps(v2)
                    ni2 = str(i2)
                    dic2[ni2] = v2
                ni = str(i)
                dic2 = json.dumps(dic2)
                dic[ni] = dic2
            dic = json.dumps(dic)
            json.dump(dic, f)
            print("已成功存储载记忆数量:", len(self.memory))

    def plain(self, v):
        """state 编码器"""
        ret = {}
        idx = 0
        for i in v:
            for j in i:
                x = 0
                for k in j:
                    if k > 0:
                        x += 1
                    x *= 2
                ret[str(idx)] = str(x)
                idx += 1
        return ret

    def build(self, ret):
        """state 解码器"""
        v = np.empty([10, 16, 16], dtype=int)
        idx = 0
        for i in range(10):
            for j in range(16):
                nidx = str(idx)
                x = int(ret[nidx])
                idx += 1
                for k in range(15, -1, -1):
                    x //= 2
                    v[i][j][k] = x & 1
        return v

def diff(a, b):
    for i in range(2):
        for j in range(5):
            if j == 0 or j == 3:
                if (a.memory[i][j].all() == b.memory[i][j].all()):
                    return True
                else:
                    return False
            else:
                if (a.memory[i][j] == b.memory[i][j]):
                    return True
                else:
                    return False

class Model(nn.Module):

    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(4, 64, kernel_size=3, stride=1, padding=0)
        self.conv2 = nn.Conv2d(64, 128, kernel_size=3, stride=1, padding=0)
        self.conv3 = nn.Conv2d(128, 256, kernel_size=3, stride=1, padding=0)
        self.conv4 = nn.Conv2d(256, 256, kernel_size=3, stride=1, padding=0)

    def save(self):
        torch.save(self, "./assist_data/Q_net.pkl")
        with open("assist_data/Q_state.json", "w+") as f:
            c = f.read()
            if f.readline() != "":
                dic = json.loads(c)
                if dic is None:
                    dic = {}
            else:
                dic = {}
            dic["net_state"] = 1
            json.dump(dic, f)


def newModel():
    flag = 0
    with open("assist_data/Q_state.json", "r") as f:
        dic = json.loads(f.read())
        if dic is not None and "net_state" in dic:
            if dic["net_state"] is not None and dic["net_state"] == 1:
                flag = 1
    if flag:
        return torch.load("./assist_data/Q_net.pkl")
    else:
        return None

if __name__ == '__main__':
    mod = Model()
    mod.save()
    mod2 = newModel()
    # a = Test()
    # state = np.ones([10, 16, 16], dtype=int)
    # tmp = Transition(state, 9, 9.9, -state, True)
    # a.memory.append(tmp)
    # a.memory.append(tmp)
    # a.save()
    # b = Test()
    # b.load()
    # if diff(a, b):
    #     print("ok")
    # else:
    #     print("fuck")
    # b.save()
    # c = Test()
    # c.load()
    # if diff(a, c):
    #     print("ok")
    # else:
    #     print("fuck")
    # print(a.memory[0])