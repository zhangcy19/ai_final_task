#interface.py

#接口，实现与游戏的交互

from sys import path
from tkinter.constants import N
import grab
import recognition
import pyautogui
import cv2
import os

class MyAPI():
    def __init__(self):
        self.Image = grab.MyImage()
        self.Assistant = recognition.MyAssitant()
        self.step = 0
        self.state_buf = None
        self.state_cur = None
        self.path = ""
        self.score = 0
        self.initScore()

        self.step_limit = 10
        self.wait_time = 1.0
    
    def getFruitState(self):
        return self.state_cur
    
    def getRange(self):
        print("\n获取游戏窗口的坐标范围...")
        return self.Image.x1, self.Image.x2

    def getXYRange(self):
        print("\n获取游戏窗口的X, Y坐标范围...")
        return self.Image.x1, self.Image.y1, self.Image.x2, self.Image.y2

    def putFruit(self, x):
        print("在x = %d 处放置水果..."%x)
        self.Assistant.x_put = x
        pyautogui.click(x, (self.Image.y1+self.Image.y2)//2)
        self.step += 1

    def getScore(self):
        os.system(f"python readData.py {self.path}\*.json")
        with open("assist_data\score.txt", "r") as f:
            self.score = f.read()
        return self.score

    def gameOver(self):
        if len(self.state_cur[0]) == 0 and self.step >= 10:
            print("游戏结束，退出")
            return True
        if self.step > self.step_limit:
            print("步数达到设定值，退出")
            return True
        return False

    def gameStable(self):
        if self.step == 0:
            return True
        if len(self.state_cur[0]) == len(self.state_buf[0]):
            return True
        else:
            return False

    def updateState(self):
        print("\n更新游戏状态...")
        self.state_buf = self.state_cur
        self.state_cur = self.Assistant.run(self.Image.getImage(), self.Image.x2, self.Image.y1, self.Image.y2)

    def setWaitTime(self, time):
        self.wait_time = time
    
    def setStepLimit(self, limit):
        self.step_limit = limit

    def visualize(self, str):
        self.Assistant.visualize = str
    
    def setFix(self, fix):
        self.Assistant.fix = fix
        self.Image.fix = fix
    
    def output(self, name):
        os.system("python saveImage.py %s output\*.png "%name)
        os.system("del output\*.png")

    def getPath(self):
        print("调试：提供路径，浏览器文件下载的绝对路径（示例：/Users/zhangcy19/Downloads）(确保该文件夹下无其他文件)")
        print("在线测试：直接回车")
        self.path = input("请输入：")
        if self.path != "":
            print("设定完成，当前分数路径：%s\n"%self.path)
        else:
            print("设定完成，在线测试模式")
        with open("assist_data\path.txt", "w") as f:
            f.write(self.path)
        self.initPath()

    def loadPath(self):
        with open("assist_data\path.txt", "r") as f:
            self.path = f.read()
        self.initPath()

    def initPath(self):
        if self.path == "":
            return
        with open(self.path + "\score.json", "w") as f:
            f.write("0")
        with open("assist_data\score.txt", "w") as f:
            f.write(str(self.score))
    
    def initScore(self):
        with open("assist_data\score.txt", "w") as f:
            f.write("0")