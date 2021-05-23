#reinforcementAI.py

#基于强化学习的AI算法

#api提供接口：
#操作类：
#  updateState()->None：更新游戏状态
#  getFruitState()->list：获取游戏状态state（变量state是一个嵌套列表，
#       对于某一个水果i，state[0][i]为水果种类，state[1][i]为该水果中心点x坐标，
#       state[2][i]为中心点y坐标）
#  putFruit(int)->None：根据传入x坐标放置水果
#状态类：
#  getRange()->（int, int）：获取游戏窗口在x轴方向范围
#  getScore()->int：返回分数 
#  gameOver()->bool：返回游戏是否结束，结束为true   
#  gameStable()->bool：返回游戏状态是否稳定，稳定为true
#设定类：
#  setWaitTime(int)->None：
#  setStepLimit(int)->None
#  setFix(int)->None

def MyAI(api):
    print("hello, world!")