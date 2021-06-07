#heuristicAI.py

#基于启发式函数的AI算法

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
import random

def MyAI(api):
    api.setWaitTime(0.25)
    api.setStepLimit(9999)
    api.setFix(1)
    start, end = api.getRange()
    print("坐标范围是:(%d, %d)" %(start, end))

    score_ratio, height_ratio = 2, 0.05
    size = [24.7, 38, 51.3, 56.5, 72.2, 87, 91.7, 122.6, 146.3, 146.3, 193.8]

    while(True):
        api.updateState()
        #print("当前分数：",api.getScore())
        if api.gameOver():
            break
        if not api.gameStable():
            print("游戏状态不稳定，等待中...")
            time.sleep(api.wait_time)
            continue
        print("计算中...")
        state = api.getFruitState()
        if len(state[0]) == 0:
            print("[Error!]：窗口中没有任何水果!")
            continue
        
        if len(state[0]) <= 2:
            api.putFruit(random.randint(start,end))
            continue

        to_put = state[2].index(min(state[2]))
        bottom = [i for i in range(len(state[0])) if i != to_put]

        best,score = [0], -999999
        for n in range(10, end, 10):
            temp_score = 0
            temp_fruit = [state[0][x] for x in bottom]
            temp_x = [state[1][x] for x in bottom]
            temp_y = [state[2][x] for x in bottom]
            t1, t2, t3, flag = state[0][to_put], n, 920-int(size[state[0][to_put]]), True
            for i in bottom:
                if abs(n-state[1][i]) < size[state[0][i]] + size[state[0][to_put]]:
                    t3 = min(t3,state[2][i]-((size[state[0][i]]+size[state[0][to_put]])**2-(n-state[1][i])**2)**0.5)
            
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
                        if ((temp_x[i]-temp_x[j])**2+(temp_y[i]-temp_y[j])**2)**0.5<2.5*size[temp_fruit[i]]:
                            rm1, rm2, flag = i, j, not flag
                            t1, t2, t3 = temp_fruit[i]+1, (temp_x[i]+temp_x[j])/2, max(temp_y[i],temp_y[j])
                            temp_score += temp_fruit[i]
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
                a = (state[1][to_put] - temp_x[i]) / (state[2][to_put] - temp_y[i])
                b = state[1][to_put] - a * state[2][to_put]
                flag = 0
                for j in range(len(temp_fruit)):
                    if j == i:
                        continue
                    if temp_y[j]>temp_y[i] and abs(a*temp_y[j]-temp_x[j]+b)/((a*a+1)**0.5)<size[temp_fruit[j]]:
                        flag = 1
                        break
                if flag == 0:
                    access.append(i)

            temp_score = temp_score * score_ratio + min(temp_y) * height_ratio + len(access)
            if temp_score > score:
                best,score = [n],temp_score
            elif temp_score == score:
                best.append(n)
        api.putFruit(best[random.randint(0,len(best)-1)]+random.randint(-9,9))
    api.output("sample.gif")
