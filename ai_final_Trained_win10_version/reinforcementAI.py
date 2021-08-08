"""
    reinforcementAI.py
    基于强化学习的AI算法
"""
#reinforcementAI.py

#基于强化学习的AI算法

#api提供接口：
#操作类：
#  updateState()->None：更新游戏状态
#  getFruitState()->list：获取游戏状态state（变量state是一个嵌套列表，
#       对于某一个水果i，state[0][i]为水果种类，state[1][i]为该水果中心点x坐标，
#       state[2][i]为中心点y坐标）
#  putFruit(int)->None：根据传入x坐标放置水果（x为绝对坐标）
#  output(str)->None：将过程图片转化为gif，保存到output文件夹中,需要提供文件名str
#       注意：相同的名字会覆盖旧文件
#状态类：
#  getRange()->（int, int）：获取游戏窗口在x轴方向范围
#  getScore()->int：返回分数 
#  gameOver()->bool：返回游戏是否结束，结束为true   
#  gameStable()->bool：返回游戏状态是否稳定，稳定为true
#设定类：
#  setWaitTime(double)->None：监测到状态在变化时等待的时间，单位为秒
#  setStepLimit(int)->None：最大步数限制
#  setFix(double)->None：屏幕坐标与图像绘制之间的换算系数，如果出现操作区域与选择区域不重合的问题请尝试修改此值

import time
import torch
import random
import modelsRL
import numpy as np

class GameEnv(object):
    """
        游戏图像处理api与deepQearning的交互接口
    """
    def __init__(self, api):
        self.state_layer_size = 10
        self.state_row_size = 16
        self.state_col_size = 16

        self.api = api
        self.state = None
        self.score = 0
        self.oldHeuristic = 0
        "self.cord[4] : x1, y1, x2, y2"
        self.cord = api.getXYRange()
        "self.inter[2] : xInterval, yInterval"
        self.inter = [((self.cord[2] - self.cord[0]) / self.state_col_size), ((self.cord[3] - self.cord[1]) / self.state_row_size)]

    def reset(self):
        self.api.updateState()
        fruitState = self.api.getFruitState()
        self.transState(fruitState)
        return self.state.detach().cpu().numpy()

    def step(self, action_x):
        """ 返回 next_state, reward, done """
        self.api.updateState()
        x = self.cord[0] + (0.5 + action_x) * self.inter[0]
        self.api.putFruit(int(x))
        fruitState = self.api.getFruitState()
        self.transState(fruitState)
        newScore = str(self.api.getScore())
        newScore = newScore.strip(u'\ufeff')
        newScore = int(newScore)
        newHeurisitc = self.heuristic()
        reward = newScore + newHeurisitc - self.score - self.oldHeuristic
        self.score = newScore
        self.oldHeuristic = newHeurisitc
        done = self.api.gameOver()
        state = self.state.detach().cpu().numpy()
        return state, reward, done

    def transState(self, fruitState):
        """ 将连续的坐标离散化并存入self.state """
        self.state = torch.zeros(self.state_layer_size, self.state_row_size, self.state_col_size)
        for i in range(len(fruitState[0])):
            x, y = fruitState[1][i], fruitState[2][i]
            nx = (x - self.cord[0]) // self.inter[0]
            ny = (y - self.cord[1]) // self.inter[1]
            nx = max(min(int(nx), 16), 0)
            ny = max(min(int(ny), 16), 0)
            st = max(min(fruitState[0][i], 9), 0)
            self.state[st][nx][ny] += 1

    def heuristic(self):
        access, size = [], [24.7, 38, 51.3, 56.5, 72.2, 87, 91.7, 122.6, 146.3, 146.3, 193.8]
        
        top_t, top_x, top_y = 0, 0, self.state.shape[2]
        for i in range(self.state.shape[0]):
            for j in range(self.state.shape[1]):
                for k in range(self.state.shape[2]):
                    if k < top_y:
                        top_t, top_x, top_y = i, j, k

        temp_fruit, temp_x, temp_y = [], [], []
        for i in range(self.state.shape[0]):
            for j in range(self.state.shape[1]):
                for k in range(self.state.shape[2]):
                    if (self.state[i][j][k] > 0) and (not(i == top_t and j == top_x and k == top_y)):
                        temp_fruit.append(i)
                        temp_x.append(j)
                        temp_y.append(k)

        for i in range(len(temp_fruit)):
            if top_y == temp_y[i]:
                if self.inter[0] * abs(top_x - temp_x[i]) >= size[temp_fruit[i]]:
                    access.append(i)
                continue
            a = (self.inter[0] * (top_x - temp_x[i])) / (self.inter[1] * (top_y - temp_y[i]))
            b = self.inter[0] * top_x - a * self.inter[1] * top_y
            flag = 0
            for j in range(len(temp_fruit)):
                if j == i:
                    continue
                if temp_y[j] > temp_y[i] and abs(a*self.inter[1]*temp_y[j]-self.inter[0]*temp_x[j]+b)/((a*a+1)**0.5)<size[temp_fruit[j]]:
                    flag = 1
                    break
            if flag == 0:
                access.append(i)
        if len(temp_fruit) != 0:
            return max(temp_fruit) * len(access) / len(temp_fruit) - max(temp_y) / (size[max(temp_fruit)] / self.inter[1])
        else:
            return 0

    def newHeuri(self):
        best_index, best_score = [0], -999999
        for n in range(self.state_col_size):
            temp_score, access, size = 0, [], [24.7, 38, 51.3, 56.5, 72.2, 87, 91.7, 122.6, 146.3, 146.3, 193.8]
            
            top_t, top_x, top_y = 0, 0, self.state.shape[2]
            for i in range(self.state.shape[0]):
                for j in range(self.state.shape[1]):
                    for k in range(self.state.shape[2]):
                        if k < top_y:
                            top_t, top_x, top_y = i, j, k

            temp_fruit, temp_x, temp_y = [], [], []
            for i in range(self.state.shape[0]):
                for j in range(self.state.shape[1]):
                    for k in range(self.state.shape[2]):
                        if (self.state[i][j][k] > 0) and (not(i == top_t and j == top_x and k == top_y)):
                            temp_fruit.append(i)
                            temp_x.append(j)
                            temp_y.append(k)

            t1, t2, t3, flag = top_t, n, 920-int(size[top_t]), True
            for i in range(len(temp_fruit)):
                if abs(n-temp_x[i]) * self.inter[0] < size[temp_fruit[i]] + size[top_t]:
                    t3 = min(t3,temp_y[i]-(((size[temp_fruit[i]]+size[top_t])**2-(self.inter[0]*(n-temp_x[i]))**2)**0.5)//self.inter[1])
                
            while flag:
                flag = not flag
                temp_fruit.append(t1)
                temp_x.append(t2)
                temp_y.append(t3)
                rm1, rm2 = -1, -1
                for i in range(len(temp_fruit)):
                    for j in range(len(temp_fruit)):
                        if i == j or temp_fruit[i] != temp_fruit[j]:
                            continue
                        if (((temp_x[i]-temp_x[j])*self.inter[0])**2+((temp_y[i]-temp_y[j])*self.inter[1])**2)**0.5<2.5*size[temp_fruit[i]]:
                            rm1, rm2, flag = i, j, not flag
                            t1, t2, t3 = temp_fruit[i]+1, (temp_x[i]+temp_x[j])//2, max(temp_y[i],temp_y[j])
                            temp_score += (temp_fruit[i] + 1)
                            break
                    if flag:
                        temp_fruit.remove(temp_fruit[max(rm1,rm2)])
                        temp_x.remove(temp_x[max(rm1,rm2)])
                        temp_y.remove(temp_y[max(rm1,rm2)])
                        temp_fruit.remove(temp_fruit[min(rm1,rm2)])
                        temp_x.remove(temp_x[min(rm1,rm2)])
                        temp_y.remove(temp_y[min(rm1,rm2)])
                        break

            access = []
            for i in range(len(temp_fruit)):
                if top_y == temp_y[i]:
                    if self.inter[0] * abs(top_x - temp_x[i]) >= size[temp_fruit[i]]:
                        access.append(i)
                    continue
                a = (self.inter[0] * (top_x - temp_x[i])) / (self.inter[1] * (top_y - temp_y[i]))
                b = self.inter[0] * top_x - a * self.inter[1] * top_y
                flag = 0
                for j in range(len(temp_fruit)):
                    if j == i:
                        continue
                    if temp_y[j] > temp_y[i] and abs(a*self.inter[1]*temp_y[j]-self.inter[0]*temp_x[j]+b)/((a*a+1)**0.5)<size[temp_fruit[j]]:
                        flag = 1
                        break
                if flag == 0:
                    access.append(i)

            temp_score = temp_score * 2 + len(access)
            if temp_score > best_score:
                best_index, best_score = [n], temp_score
            elif temp_score == best_score:
                best_index.append(n)
        return best_index[random.randint(0,len(best_index)-1)]

def trainMyAI(api):
    """训练函数"""
    api.setWaitTime(0.1)
    api.setStepLimit(999999)
    api.setFix(1)
    env = GameEnv(api)
    model = modelsRL.DeepQModel(env)
    for i in range(256):
        model.train_model(200)
