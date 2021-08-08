#recognition.py

#识别图像信息

import numpy as np
import cv2
from paddlex import deploy

class MyAssitant():
    def __init__(self):
        self.category = [ 'pt', 'yt', 'jz', 'nm', 'mht', 'xhs', 'tz', 'bl', 'yz', 'xg', 'dxg']
        self.load_model()
        self.count = 0
        self.tolerance = 0.3
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.fix = 2
        self.visualize = "image"
        self.x_put = -1

    def load_model(self):
        print("loading model...")
        self.det = deploy.Predictor("assist_model")
        print("loading finished!\n")

    def draw(self, datas, img, y1, y2):
        color_g = (0, 255, 0)
        color_r = (0, 0, 255)
        color_b = (255, 0, 0)
        color_black = (0, 0, 0)
        for value in datas:         
            score = value['score']
            if score < self.tolerance:
                continue
            xmin, ymin, w, h = np.array(value['bbox']).astype(np.int32)
            category = value['category']
            cv2.rectangle(img, (xmin, ymin), (xmin+w, ymin+h), color_g, 4)
            cv2.putText(img, '{:s}'.format(category),
                            (xmin, ymin), self.font, 1.0, color_black, thickness=2)
            if self.x_put >= 0:
                cv2.line(img, (self.x_put*2, y1*2), (self.x_put*2, y2*2), color_r, 4)
                cv2.putText(img, "put on x=%d"%(self.x_put*2), (self.x_put*2, y1*2),self.font, 1.0, color_black, thickness=2)
                self.x_put = -1
        return img

    def run(self, img, window_x, window_y1, window_y2):
        image = cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)
        datas = self.det.predict(image)
        category_list = []
        x_list = []
        y_list = []
        for data in datas:
            value = data["score"]
            if value < self.tolerance:
                continue
            x1, y1, w, h = np.array(data["bbox"]).astype(np.int32)
            category = data["category_id"]
            category_list.append(category)
            x_list.append(int((x1 + w/2) / self.fix))
            y_list.append(int((y1 + h/2) / self.fix))
        if self.visualize == "image":   
            image = self.draw(datas, image, window_y1, window_y2)
            cv2.imwrite("output/img{}.png".format(self.count), image)
            self.count += 1
        elif self.visualize == "video": 
            image = self.draw(datas, image, window_y1, window_y2)
            cv2.imwrite("output/img{}.png".format(self.count), image)
            self.count += 1
            cv2.moveWindow("window", window_x+20, 0)
            cv2.imshow("window", image)
            cv2.waitKey(100)
        return category_list, x_list, y_list