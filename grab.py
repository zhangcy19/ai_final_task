#grab.py

#截取游戏图片
#测试版本，考虑到win32gui的兼容性所以没有使用，改用tkinter手动框选得到窗口位置
#后续的移动端版本根据机型直接得到窗口信息？

import tkinter
from PIL import ImageGrab
import json

class MyImage:
    def __init__(self):
        self.x1, self.y1 = 0, 0
        self.x2, self.y2 = 1, 1
        self.area = None
        self.fix = 2
    
    def getArea(self):  
        print("设定区域：鼠标拖动以框选，按esc中断操作")     
        root = tkinter.Tk()
        root.attributes("-alpha", 0.3)
        root.overrideredirect(True)
        root.configure(bg="black")
        root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight())) 
        #print(root.winfo_screenwidth(), root.winfo_screenheight())      
        cv = tkinter.Canvas(root)

        def exitMotion(event):
            root.destroy()

        def getFirstPoint(event):
            self.x1 ,self.y1 = event.x, event.y
            cv.configure(height=1)
            cv.configure(width=1)
            cv.configure(highlightthickness=0)
            cv.place(x=self.x1, y=self.y1)
            self.area = cv.create_rectangle(0, 0, 0, 0, outline='red', width=1, dash=(4, 4))

        def changeWindow(event):
            self.x2 ,self.y2 = event.x, event.y
            cv.configure(height=self.y2 - self.y1)
            cv.configure(width=self.x2 - self.x1)
            cv.coords(self.area, 0, 0, self.x2 - self.x1, self.y2 - self.y1)

        def getSecondPoint(event):
            self.x2, self.y2 = event.x, event.y
            print("设定完成，当前区域:（%d，%d）至（%d， %d）\n"%(self.x1, self.y1, self.x2, self.y2))
            #print(self.x1, self.y1, self.x2, self.y2)
            exitMotion(None)
         
        root.bind("<Button-1>", getFirstPoint)
        root.bind("<B1-Motion>", changeWindow)
        root.bind("<ButtonRelease-1>", getSecondPoint)
        root.bind("<Escape>",exitMotion)
        root.mainloop()

    def getImage(self):
        x1 = self.x1 * self.fix
        y1 = self.y1 * self.fix
        x2 = self.x2 * self.fix
        y2 = self.y2 * self.fix
        image = ImageGrab.grab((x1, y1, x2, y2))
        #image.save("test.png")
        return image

    def saveArea(self):
        info = [self.x1, self.y1, self.x2, self.y2]
        #print(self.x1, self.y1, self.x2, self.y2)
        with open("assist_data/area.json", "w") as f:
            json.dump(info, f)
    
    def loadArea(self):
        with open("assist_data/area.json", "r") as f:
            self.x1, self.y1, self.x2, self.y2 = json.loads(f.read()) 
            #print(self.x1, self.y1, self.x2, self.y2)