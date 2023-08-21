import cv2
import numpy as np
import datetime

# 開啟網路攝影機
cap = cv2.VideoCapture(1)

# 編碼方式：XVID
fourcc = cv2.VideoWriter_fourcc(*'XVID')
w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
# 輸出影像 = （格式, 來源, FPS, 影像長寬）
out = cv2.VideoWriter('output.mp4', fourcc, 20.0, (w,h))

# 設定擷取影像的尺寸大小
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

# 編碼方式：XVID
# fourcc = cv2.VideoWriter_fourcc(*'XVID')
# out = cv2.VideoWriter('VideoOutput.mp4', fourcc, 20.0, (640, 480))

# 初始化平均影像
# ret boolean value = 判斷是否讀取成功
# frame = 每個影格
ret, frame = cap.read()
avg = cv2.blur(frame, (4, 4))
avg_float = np.float32(avg)

while(cap.isOpened()):
  # 讀取一幅影格
  ret, frame = cap.read()

  # 若讀取至影片結尾，則跳出
  if ret == False:
    break

  # 顯示當前時間，視窗解析度
  font = cv2.FONT_HERSHEY_SIMPLEX
  text = 'Width ' + str(cap.get(3)) + '  ' +'Height ' + str(cap.get(4))
  date = str(datetime.datetime.now())
  frame = cv2.putText(frame, text, (10, 50), font, 1,
                      (0, 255, 255), 2, cv2.LINE_AA)
  frame = cv2.putText(frame, date, (10, 100), font, 1,
                      (0, 255, 255), 2, cv2.LINE_AA)

  # 模糊處理
  blur = cv2.blur(frame, (4, 4))

  # 計算目前影格與平均影像的差異值
  different = cv2.absdiff(avg, blur)

  # 將圖片轉為灰階
  gray = cv2.cvtColor(different, cv2.COLOR_BGR2GRAY)

  # 篩選出變動程度大於門檻值的區域
  # 影像二值化（灰階影像, 像素灰階門檻值, 像素灰階最大值, 二值化類型）
  # 即傳入灰階影像的灰階值 > 門檻值：設為灰階最大值，否則設為0
  ret, thresh = cv2.threshold(gray, 25, 255, cv2.THRESH_BINARY)

  # 使用型態轉換函數去除雜訊
  kernel = np.ones((5, 5), np.uint8)
  # 開運算
  thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)
  # 閉運算
  thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=2)

  # 產生等高線
  # 尋找輪廓（二值化圖像, 輪廓檢索方式：外部輪廓, 輪廓近似方法：壓縮水平、垂直、對角線段、垂直、對角線段，留下四端點）
  # 回傳值 cnts = 輪廓, _ = 階層（暫時不需）
  cnts, _= cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

  for c in cnts:
    if cv2.contourArea(c) > 250000 and cv2.contourArea(c) < 1000000:
      
      # 偵測到物體
      # 計算等高線的外框範圍
      (x, y, w, h) = cv2.boundingRect(c)
      cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
      print(cv2.contourArea(c))
      
  # 畫出等高線（測試）
  # 畫出輪廓（要畫的圖片, 先前找出的輪廓 cnts, -1 = 所有找到的輪廓點, 顏色, 線條粗度）
  cv2.drawContours(frame, cnts, -1, (0, 255, 255), 2)
  

  out.write(frame)
  # 顯示偵測結果影像
  cv2.imshow('frame', frame)
  # 'Q'鍵中斷程式
  if cv2.waitKey(1) & 0xFF == ord('q'):
      break

  # 更新平均影像
  cv2.accumulateWeighted(blur, avg_float, 0.01)
  avg = cv2.convertScaleAbs(avg_float)

cap.release()
out.release()
cv2.destroyAllWindows()