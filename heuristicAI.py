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

def MyAI(api):
    print("hello, world!")