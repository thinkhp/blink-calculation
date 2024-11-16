# -*- coding: utf-8 -*-
import cv2
import dlib
import numpy as np
from scipy.spatial import distance
import sys
import time

def calculate_EAR(eye):
    """Calculate Eye Aspect Ratio"""
    A = distance.euclidean(eye[1], eye[5])
    B = distance.euclidean(eye[2], eye[4])
    C = distance.euclidean(eye[0], eye[3])
    ear = (A + B) / (2.0 * C)
    return ear

def detect_blinks(shape, FACIAL_LANDMARKS_68_IDXS):
    """Detect Eye Blinks"""
    (lStart, lEnd) = FACIAL_LANDMARKS_68_IDXS["left_eye"]
    (rStart, rEnd) = FACIAL_LANDMARKS_68_IDXS["right_eye"]
    
    leftEye = shape[lStart:lEnd]
    rightEye = shape[rStart:rEnd]
    
    leftEAR = calculate_EAR(leftEye)
    rightEAR = calculate_EAR(rightEye)
    
    ear = (leftEAR + rightEAR) / 2.0
    return ear, leftEAR, rightEAR

def main():
    # Check command line arguments
    camera_index = 0
    if len(sys.argv) > 1:
        camera_index = int(sys.argv[1])

    # Initialize detector
    try:
        detector = dlib.get_frontal_face_detector()
        predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')
    except RuntimeError as e:
        print(f"Error: Cannot load the facial landmark detector model file.\n{str(e)}")
        return
    
    FACIAL_LANDMARKS_68_IDXS = {
        "left_eye": (42, 48),
        "right_eye": (36, 42),
    }
    
    # 调整这些参数来优化眨眼检测
    EAR_THRESHOLD = 0.25        # 提高阈值，使检测更敏感
    CONSEC_FRAMES = 1          # 减少需要的连续帧数
    MIN_BLINK_INTERVAL = 0.1   # 最小眨眼间隔（秒）
    
    COUNTER = 0
    TOTAL = 0
    
    # 用于存储EAR历史值的列表
    ear_history = []
    history_length = 10  # 保存最近10帧的EAR值
    
    # Open camera
    print(f"Trying to open camera {camera_index}...")
    cap = cv2.VideoCapture(camera_index)
    
    if not cap.isOpened():
        print("Error: Cannot open camera. Please check:")
        print("1. Camera access is allowed in System Preferences")
        print("2. Camera is not being used by other applications")
        print("3. Try different camera indices (0, 1, 2...)")
        return
    
    # Set camera resolution
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)  # 降低分辨率以提高性能
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    print("Camera started. Press 'q' to quit.")
    print(f"Current EAR threshold: {EAR_THRESHOLD}")
    
    last_blink_time = time.time()
    fps_time = time.time()
    frame_count = 0
    fps = 0
    
    # 用于绘制EAR图表的设置
    graph_width = 200
    graph_height = 100
    graph_data = []
    
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Cannot read camera frame")
                break
            
            # Calculate FPS
            frame_count += 1
            if time.time() - fps_time >= 1.0:
                fps = frame_count
                frame_count = 0
                fps_time = time.time()
            
            # Image processing
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = detector(gray, 0)
            
            # 创建一个用于显示EAR图表的图像
            graph = np.ones((graph_height, graph_width, 3), dtype=np.uint8) * 255
            
            for face in faces:
                shape = predictor(gray, face)
                shape = np.array([[p.x, p.y] for p in shape.parts()])
                
                ear, leftEAR, rightEAR = detect_blinks(shape, FACIAL_LANDMARKS_68_IDXS)
                
                # 更新EAR历史
                ear_history.append(ear)
                if len(ear_history) > history_length:
                    ear_history.pop(0)
                
                # 计算EAR的平均值和标准差
                avg_ear = np.mean(ear_history)
                
                # 检测眨眼
                current_time = time.time()
                if ear < EAR_THRESHOLD and (current_time - last_blink_time) > MIN_BLINK_INTERVAL:
                    COUNTER += 1
                else:
                    if COUNTER >= CONSEC_FRAMES:
                        TOTAL += 1
                        last_blink_time = current_time
                    COUNTER = 0
                
                # 在每只眼睛周围画框
                for eye_points in [shape[36:42], shape[42:48]]:  # 左眼和右眼的点
                    eye_points = eye_points.astype(np.int32)
                    cv2.polylines(frame, [eye_points], True, (0, 255, 0), 1)
                
                # 显示信息
                cv2.putText(frame, f"Blinks: {TOTAL}", (10, 30),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                cv2.putText(frame, f"EAR: {ear:.3f}", (10, 60),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                cv2.putText(frame, f"Avg EAR: {avg_ear:.3f}", (10, 90),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                cv2.putText(frame, f"FPS: {fps}", (10, 120),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                
                # 更新图表数据
                graph_data.append(ear)
                if len(graph_data) > graph_width:
                    graph_data.pop(0)
                
                # 绘制EAR图表
                for i in range(len(graph_data) - 1):
                    pt1 = (i, int(graph_height - (graph_data[i] * graph_height)))
                    pt2 = (i + 1, int(graph_height - (graph_data[i + 1] * graph_height)))
                    cv2.line(graph, pt1, pt2, (0, 0, 255), 1)
                
                # 绘制阈值线
                threshold_y = int(graph_height - (EAR_THRESHOLD * graph_height))
                cv2.line(graph, (0, threshold_y), (graph_width, threshold_y), (0, 255, 0), 1)
            
            # 显示图表
            cv2.imshow("EAR Graph", graph)
            
            # Show main image
            cv2.imshow("Blink Detection", frame)
            
            # 按键处理
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                print("\nProgram exit normally")
                break
            elif key == ord('+'): # 增加阈值
                EAR_THRESHOLD += 0.01
                print(f"EAR threshold increased to: {EAR_THRESHOLD:.2f}")
            elif key == ord('-'): # 减少阈值
                EAR_THRESHOLD -= 0.01
                print(f"EAR threshold decreased to: {EAR_THRESHOLD:.2f}")
            
    except KeyboardInterrupt:
        print("\nDetected Ctrl+C, exiting...")
    finally:
        # Release resources
        cap.release()
        cv2.destroyAllWindows()
        print(f"Total blinks detected: {TOTAL}")

if __name__ == "__main__":
    main()