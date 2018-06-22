#-*- coding: utf-8 -*-
import os  
import cv2
import sys
from PIL import Image
import threading
import time
from threading import Thread
import pygame

pygame.mixer.init() 
pygame.mixer.music.load("hey.mp3")

# 定义异步装饰器
def async(f):
    def wrapper(*args, **kwargs):
        thr = Thread(target = f, args = args, kwargs = kwargs)
        thr.start()
    return wrapper

threadLock = threading.Lock()

#@async
def play_sounds():  
    #threadLock.acquire()
    if not pygame.mixer.music.get_busy():
        pygame.mixer.music.play()
        #time.sleep(0.2)
    # threadLock.release()


def stop_sounds():
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.stop()

def CatchUsbVideo(window_name, camera_idx):
    cv2.namedWindow(window_name)
    
    #视频来源，可以来自一段已存好的视频，也可以直接来自USB摄像头
    cap = cv2.VideoCapture(camera_idx)                
    
    #告诉OpenCV使用人脸识别分类器
    classfier = cv2.CascadeClassifier("/usr/local/share/OpenCV/haarcascades/haarcascade_frontalface_alt2.xml")
    
    #识别出人脸后要画的边框的颜色，RGB格式
    color = (0, 255, 0)
    count = 0    
    while cap.isOpened():
    # while True:
        ok, frame = cap.read() #读取一帧数据
        if not ok:            
            break  

        #将当前帧转换成灰度图像
        grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)                 
                
        #人脸检测，1.2和2分别为图片缩放比例和需要检测的有效点数
        faceRects = classfier.detectMultiScale(grey, scaleFactor = 1.2, minNeighbors = 3, minSize = (32, 32))
        if len(faceRects) > 0:#大于0则检测到人脸
            count += 1
            print("Hey! " + str(count))
            for faceRect in faceRects:  #单独框出每一张人脸
                x, y, w, h = faceRect        
                cv2.rectangle(frame, (x - 10, y - 10), (x + w + 10, y + h + 10), color, 2)
            play_sounds()

        else:
            print("No face detected.")
            stop_sounds()
        #显示图像
        
        cv2.imshow(window_name, frame)        
        c = cv2.waitKey(10)
       
        if c & 0xFF == ord('q'):
            break       

    #释放摄像头并销毁所有窗口
    cap.release()
    cv2.destroyAllWindows() 

    
if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage:%s camera_id\r\n" % (sys.argv[0]))
    else:
        CatchUsbVideo("识别人脸区域", int(sys.argv[1]))
       # play_sounds()
        
