import cv2
import pyvirtualcam

video_url = "rtmp://127.0.0.1:1935/live/channel0"
cap = cv2.VideoCapture(video_url)

if not cap.isOpened():
    print("无法打开视频流")
    exit()

# 尝试读取第一帧来获取分辨率和帧率
ret, frame = cap.read()
if not ret:
    print("无法读取视频帧")
    exit()

height, width = frame.shape[:2]
fps = cap.get(cv2.CAP_PROP_FPS)
if fps == 0 or fps is None:
    fps = 30  # 设置一个默认帧率

print(f"📷 视频流分辨率: {width}x{height}, FPS: {fps}")

# 初始化虚拟摄像头（只初始化一次）
with pyvirtualcam.Camera(width=width, height=height, fps=int(fps), print_fps=False) as cam:
    print(f"✅ 虚拟摄像头已打开: {cam.device}")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("⚠️ 视频流结束或读取失败")
            break
        
        # 显示画面
        # cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
        # 转换颜色 & 发送到虚拟摄像头
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        cam.send(frame_rgb)
        cam.sleep_until_next_frame()

cap.release()
cv2.destroyAllWindows()