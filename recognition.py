#recognition.py

#识别图像信息

import numpy as np
import cv2
from paddlex import deploy

class MyAssitant():
    def __init__(self):
        self.x1, self.y1 = 0, 0
        self.x2, self.y2 = 1, 1
        self.category = [
            'pt', 'yt', 'jz', 'nm',
            'mht', 'xhs', 'tz', 'bl', 'yz', 'xg', 'dxg'
        ]       
        self.size = {
            'pt': 10, 'yt': 15,
            'jz': 20, 'nm': 25,
            'mht': 30, 'xhs': 35,
            'tz': 40, 'bl': 50,
            'yz': 55, 'xg': 60
        } 
        self.load_model()
        self.count = 0
        self.tolerance = 0.3
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.fix = 2
        self.visualize = "off"

    def load_model(self):
        print("loading model...")
        self.det = deploy.Predictor("assist_model")
        print("loading finished!\n")

    def draw(self, datas, img):
        color = (0, 255, 0)
        for value in datas:         
            score = value['score']
            if score < self.tolerance:
                continue
            xmin, ymin, w, h = np.array(value['bbox']).astype(np.int)
            category = value['category']
            cv2.rectangle(img, (xmin, ymin), (xmin+w, ymin+h), color, 4)
            cv2.putText(img, '{:s}'.format(category),
                            (xmin, ymin), self.font, 1.0, (255, 0, 0), thickness=2)
        return img

    def run(self, img, ls):
        self.x1, self.y1 = ls[0], ls[1]
        self.x2, self.y2 = ls[2], ls[3]
          
        image = cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)
        datas = self.det.predict(image)
        category_list = []
        x_list = []
        y_list = []
        for data in datas:
            value = data["score"]
            if value < self.tolerance:
                continue
            x1, y1, w, h = np.array(data["bbox"]).astype(np.int)
            category = data["category_id"]
            category_list.append(category)
            x_list.append(int((x1 + w/2) / self.fix))
            y_list.append(int((y1 + h/2) / self.fix))
        #print(category_list)
        #print(x_list)
        #print(y_list)
        if self.visualize == "image":   
            image = self.draw(datas, image)
            cv2.imwrite("output/img{}.png".format(self.count), image)
            self.count += 1
        elif self.visualize == "video": 
            image = self.draw(datas, image)
            cv2.imshow("window", image)
            cv2.waitKey(100)      
        return category_list, x_list, y_list