import os
from moviepy.editor import *
import cv2

# 輸出目錄
outputFolder = "My_output_test"

# 自動建立目錄
if not os.path.exists(outputFolder):
  os.makedirs(outputFolder)

# 開啟影片檔
video = VideoFileClip("oxxostudio.mp4")
cap = cv2.VideoCapture(video)

# 取得畫面尺寸
width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

while(cap.isOpened()):
  # 讀取一幅影格
  ret, frame = cap.read()

  # 若讀取至影片結尾，則跳出
  if ret == False:
    break
  
  frame = video.save_frame("frame1.jpg", t = 5)
  frame = video.save_frame("frame2.jpg", t = 10)
  frame = video.save_frame("frame3.jpg", t = 15)
print('ok')