import cv2
import dlib
import numpy as np
from scipy.spatial import distance

def calculate_EAR(eye):
    """计算眼睛纵横比(Eye Aspect Ratio)"""
    # 计算垂直方向上的两组点之间的欧氏距离
    A = distance.euclidean(eye[1], eye[5])
    B = distance.euclidean(eye[2], eye[4])
    # 计算水平方向上的点之间的欧氏距离
    C = distance.euclidean(eye[0], eye[3])
    # 计算眼睛纵横比
    ear = (A + B) / (2.0 * C)
    return ear

def detect_blinks(shape, FACIAL_LANDMARKS_68_IDXS):
    """检测是否眨眼"""
    # 获取左眼和右眼的特征点索引
    (lStart, lEnd) = FACIAL_LANDMARKS_68_IDXS["left_eye"]
    (rStart, rEnd) = FACIAL_LANDMARKS_68_IDXS["right_eye"]

    # 提取左眼和右眼的坐标
    leftEye = shape[lStart:lEnd]
    rightEye = shape[rStart:rEnd]

    # 计算左右眼的EAR值
    leftEAR = calculate_EAR(leftEye)
    rightEAR = calculate_EAR(rightEye)

    # 计算平均EAR值
    ear = (leftEAR + rightEAR) / 2.0
    return ear

def main():
    # 初始化dlib的人脸检测器和面部特征点预测器
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

    # 定义面部特征点的索引
    FACIAL_LANDMARKS_68_IDXS = {
        "left_eye": (42, 48),
        "right_eye": (36, 42),
    }

    # 设置眨眼检测的阈值
    EAR_THRESHOLD = 0.25  # 当EAR小于此值时判定为眨眼
    CONSEC_FRAMES = 2     # 连续几帧小于阈值才算一次眨眼

    # 初始化计数器
    COUNTER = 0
    TOTAL = 0

    # 打开摄像头
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # 转换为灰度图
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # 检测人脸
        faces = detector(gray, 0)

        for face in faces:
            # 检测面部特征点
            shape = predictor(gray, face)
            shape = np.array([[p.x, p.y] for p in shape.parts()])

            # 检测眨眼
            ear = detect_blinks(shape, FACIAL_LANDMARKS_68_IDXS)

            # 检查是否眨眼
            if ear < EAR_THRESHOLD:
                COUNTER += 1
            else:
                if COUNTER >= CONSEC_FRAMES:
                    TOTAL += 1
                COUNTER = 0

            # 在图像上显示眨眼次数
            cv2.putText(frame, f"Blinks: {TOTAL}", (10, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

            # 在图像上显示EAR值
            cv2.putText(frame, f"EAR: {ear:.2f}", (300, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        # 显示图像
        cv2.imshow("Frame", frame)

        # 按'q'退出
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # 释放资源
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()