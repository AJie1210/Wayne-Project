import cv2
import os

def extract_frames(video_path, output_path, interval):
    # 開啟影片檔案
    video = cv2.VideoCapture(video_path)
    
    # 計數器
    count = 0
    
    # 讀取並提取影格
    while video.isOpened():
        # 讀取影格
        ret, frame = video.read()
        
        if not ret:
            break
        
        fps = video.get(cv2.CAP_PROP_FPS)
        print(fps)

        # 每隔固定時間間隔進行處理
        if count % interval == 0:
            # 儲存影格
            frame_path = f"{output_path}/frame{count}.jpg"
            cv2.imwrite(frame_path, frame)
        
        count += 1
    
    # 釋放資源
    video.release()
    cv2.destroyAllWindows()

# 呼叫函式並指定影片路徑、輸出路徑和時間間隔
video_path = "output.mp4"
output_path = "output_test"

if not os.path.exists(output_path):
  os.makedirs(output_path)

# 每隔20影格截圖一次(Video FPS = 20), 一秒截圖一次
# 每隔40影格截圖一次(Video FPS = 20), 兩秒截圖一次
interval = 20  

extract_frames(video_path, output_path, interval)
