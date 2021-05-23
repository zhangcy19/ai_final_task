#interface.py

#接口，实现与游戏的交互

from tkinter.constants import N
import grab
import recognition
import pyautogui

class MyAPI():
    def __init__(self):
        self.Image = grab.MyImage()
        self.Assistant = recognition.MyAssitant()
        self.area = [self.Image.x1, self.Image.y1, self.Image.x2, self.Image.y2]
        self.step = 0
        self.state_buf = None
        self.state_cur = None

        self.step_limit = 10
        self.wait_time = 1
    
    def getFruitState(self):
        return self.state_cur
    
    def getRange(self):
        print("\ngetting game window range...")
        return self.Image.x1, self.Image.x2

    def putFruit(self, x):
        print("putting fruit at %d..."%x)
        pyautogui.click(x, (self.Image.y1+self.Image.y2)//2)
        self.step += 1

    def getScore(self):
        #待完成
        return 1

    def gameOver(self):
        if len(self.state_cur[0]) == 0 and self.step != 0:
            print("game over, exit!")
            return True
        if self.step > self.step_limit:
            print("step limit exceeded, exit!")
            return True
        return False

    def gameStable(self):
        #state = self.Assistant.run(self.Image.getImage(), self.area)
        if self.step == 0:
            return True
        if len(self.state_cur[0]) == len(self.state_buf[0]):
            return True
        else:
            return False

    def updateState(self):
        print("\nupdating game state...")
        self.state_buf = self.state_cur
        self.state_cur = self.Assistant.run(self.Image.getImage(), self.area)

    def setWaitTime(self, time):
        self.wait_time = time
    
    def setStepLimit(self, limit):
        self.step_limit = limit

    def visualize(self, str):
        self.Assistant.visualize = str
    
    def setFix(self, fix):
        self.Assistant.fix = fix
        self.Image.fix = fix

    

    


