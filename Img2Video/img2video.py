import cv2
import time
import datetime

# 打开摄像头
cap = cv2.VideoCapture(0)

# 获取视频帧的宽度和高度
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))

# 设置视频保存间隔（秒）
save_interval = 10 * 60  # 10 分钟

# 初始化计时器
start_time = time.time()

# 初始化视频写入对象
out = None

while True:
    # 获取当前时间
    current_time = time.time()

    # 检查是否需要保存新的视频文件
    if current_time - start_time >= save_interval or out is None:
        # 如果之前有视频写入对象，先释放它
        if out is not None:
            out.release()

        # 生成新的文件名
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        video_name = f'output_video_{timestamp}.mp4'

        # 创建视频写入对象
        out = cv2.VideoWriter(video_name, cv2.VideoWriter_fourcc(*'mp4v'), 20, (frame_width, frame_height))

        # 重置计时器
        start_time = current_time

    ret, frame = cap.read()
    if ret:
        # 写入视频文件
        out.write(frame)

        # 显示当前帧
        cv2.imshow('Frame', frame)

        # 按 'q' 键退出循环
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

# 释放资源
cap.release()
if out is not None:
    out.release()
cv2.destroyAllWindows()
