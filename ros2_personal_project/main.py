import cv2
from ultralytics import YOLO
import time
import os

# 1. 변환된 OpenVINO 모델 경로 (xml 파일 지정)
# 방금 변환했다면 폴더 이름이 'last_openvino_model'일 겁니다.
model_path = '/home/kim/robot_ws/src/ros2_personal_project/ros2_personal_project/last_openvino_model'

if not os.path.exists(model_path):
    print(f"❌ 모델 파일을 찾을 수 없습니다: {model_path}")
    print("터미널에서 'yolo export model=last.pt format=openvino imgsz=320'를 먼저 실행했는지 확인하세요!")
    exit()

try:
    print("⏳ 로컬 환경 OpenVINO 모델 로드 중...")
    model = YOLO(model_path, task='detect')
    print("✅ 로드 성공! 실시간 감지를 시작합니다.")
except Exception as e:
    print(f"❌ 로드 실패: {e}")
    exit()

# 2. 웹캠 연결
cap = cv2.VideoCapture(0)

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        break

    frame = cv2.flip(frame, 1)  # 좌우 반전

    # 3. 추론 실행 (imgsz=320 고정, conf=0.25로 팔 인식 보완)
    results = model.predict(frame, imgsz=320, conf=0.15, agnostic_nms=True, stream=True, verbose=False)

    for r in results:
        # 화면에 박스 그리기
        annotated_frame = r.plot()

        # FPS 계산 및 표시
        # (필요하다면 여기에 로봇 제어 로직을 넣으시면 됩니다!)

        cv2.imshow("TurtleBot Vision Test (300:400:300)", annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
