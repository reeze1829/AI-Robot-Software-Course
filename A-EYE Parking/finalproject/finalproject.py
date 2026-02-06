import cv2
import sys
import numpy as np
import pickle
import pytesseract
import os
import re
import sqlite3
import math
from PIL import ImageFont, ImageDraw, Image
from ultralytics import YOLO
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer
from pathlib import Path

try:
    from Team_Project_GUI import MainWindow
except ImportError:
    print("오류: Team_Project_GUI.py 파일을 찾을 수 없습니다.")

# 1. 설정 및 전역 변수 블록
class config:
    PARKING_COORDINATES = {}
    SAVE_FILE = 'parking_coordinates.pkl'
    ENTRANCE_CODE = (320, 480) 

# 전역 변수 초기화
current_frame = None
recognized_vehicle_no = ""
cap = None
last_full_frame = None
timer = None
assigned_seats = []
model_b = None

# 2. 핵심 함수 블록 (Step 0 ~ Step 5)

def step0_initialize():
    pytesseract_path = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    if not os.path.exists(pytesseract_path):
        print("오류: Tesseract 경로를 확인해주세요.")
        return None, None
    pytesseract.pytesseract.tesseract_cmd = pytesseract_path
    
    try:
        model = YOLO('yolov8n.pt')
        return pytesseract, model
    except Exception as e:
        print(f"오류: YOLO 모델 로드 실패: {e}")
        return pytesseract, None

def step1_ocr_process(roi_frame):
    gray = cv2.cvtColor(roi_frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.resize(gray, None, fx=3, fy=3, interpolation=cv2.INTER_CUBIC)
    blur = cv2.GaussianBlur(gray, (3, 3), 0)
    _, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    raw_text = pytesseract.image_to_string(thresh, lang='kor+eng', config='--psm 7').strip()
    clean_text = re.sub(r'[^가-힣0-9]', '', raw_text)
    match = re.search(r'\d{2,3}[가-힣]\d{4}', clean_text)
    return match.group() if match else clean_text[:8]

def step2_db_check(vehicle_no):
    try:
        db_path = r'C:\Users\User\robotics\databases\parking.db'
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute("SELECT name, building_no FROM car_info WHERE vehicle_no=?", (vehicle_no,))
        row = cur.fetchone()
        conn.close()
        if row:
            return {'name': row[0], 'my_area': row[1]}
        return None
    except Exception as e:
        print(f"DB 에러: {e}")
        return None

def step3_yolo_analysis(full_frame, model_obj):
    full_frame = cv2.resize(full_frame, (640, 480))
    results = model_obj.predict(full_frame, verbose=False)
    seat_status = {name: "Empty" for name in config.PARKING_COORDINATES}
    target_classes = [0, 24, 56, 63, 77]

    for result in results:
        for box in result.boxes:
            cls_id = int(box.cls[0].cpu().numpy())
            if cls_id in target_classes and box.conf[0].cpu().numpy() > 0.25:
                ox1, oy1, ox2, oy2 = map(int, box.xyxy[0].cpu().numpy())
                foot_y1 = int(oy1 + (oy2 - oy1) * 0.7)
                for seat_name, (sx, sy, sw, sh) in config.PARKING_COORDINATES.items():
                    if max(ox1, sx) < min(ox2, sx + sw) and max(foot_y1, sy) < min(oy2, sy + sh):
                        seat_status[seat_name] = "Seat"
    return seat_status

def step4_logic_dicision(seat_status, user_name="", building_no=None):
    global assigned_seats
    empty_seats = [name for name, status in seat_status.items() if status == "Empty"]
    if not empty_seats: return None
    
    available_now = [s for s in empty_seats if s not in assigned_seats] or empty_seats
    
    if building_no == 101:
        priority_list = sorted(available_now, key=lambda x: int(re.findall(r'\d+', x)[0]))
    elif building_no == 102:
        priority_list = sorted(available_now, key=lambda x: int(re.findall(r'\d+', x)[0]), reverse=True)
    else:
        ex, ey = config.ENTRANCE_CODE
        priority_list = sorted(available_now, key=lambda s: math.sqrt(
            (config.PARKING_COORDINATES[s][0] + config.PARKING_COORDINATES[s][2]/2 - ex)**2 +
            (config.PARKING_COORDINATES[s][1] + config.PARKING_COORDINATES[s][3]/2 - ey)**2))
    
    best_seat = priority_list[0]
    assigned_seats.append(best_seat)
    return best_seat

def step5_visual_guide(frame, final_destination):
    if not final_destination: return frame, "빈 좌석이 없습니다."
    sx, sy, sw, sh = config.PARKING_COORDINATES[final_destination]
    cv2.rectangle(frame, (sx, sy), (sx + sw, sy + sh), (0, 255, 255), 3)
    return frame, f"안내: {final_destination} 구역으로 이동하세요."

# 3. GUI 이벤트 및 실행 블록

def process_frame(cap_obj):
    global current_frame, last_full_frame
    ret, frame = cap_obj.read()
    if not ret: return
    last_full_frame = frame.copy()
    display_frame = cv2.flip(frame, 1)
    
    roi_w, roi_h, roi_x, roi_y = 320, 70, 160, 370
    mirror_x = 640 - roi_x - roi_w
    cv2.rectangle(display_frame, (mirror_x, roi_y), (mirror_x + roi_w, roi_y + roi_h), (0, 255, 0), 2)
    current_frame = frame[roi_y:roi_y + roi_h, roi_x:roi_x + roi_w]

    rgb_image = cv2.cvtColor(display_frame, cv2.COLOR_BGR2RGB)
    h, w, ch = rgb_image.shape
    q_img = QImage(rgb_image.data, w, h, ch * w, QImage.Format_RGB888)
    window.bg_label.setPixmap(QPixmap.fromImage(q_img).scaled(window.bg_label.width(), window.bg_label.height()))

def on_capture_clicked():
    global recognized_vehicle_no
    if current_frame is not None:
        recognized_vehicle_no = step1_ocr_process(current_frame)
        valid = re.search(r'[가-힣]', recognized_vehicle_no) and 7 <= len(recognized_vehicle_no) <= 8
        window.update_message(f"인식 결과: {recognized_vehicle_no}" if valid else f"인식 중... ({recognized_vehicle_no})")

def on_logic_clicked():
    global recognized_vehicle_no, model_b, last_full_frame
    if not recognized_vehicle_no:
        window.update_message("먼저 번호판을 인식해 주세요.")
        return
    user_data = step2_db_check(recognized_vehicle_no)
    if user_data:
        status = step3_yolo_analysis(last_full_frame, model_b)
        seat = step4_logic_dicision(status, user_data['name'], user_data['my_area'])
        _, msg = step5_visual_guide(last_full_frame, seat)
        window.update_message(f"{user_data['name']}님, {msg}")
    else:
        window.update_message("미등록 차량입니다.")

def on_exit_clicked():
    cap.release()
    timer.stop()
    cv2.destroyAllWindows()
    QApplication.instance().quit()

def main():
    global window, model_b, cap, timer
    # 좌표 로드
    if os.path.exists(config.SAVE_FILE):
        with open(config.SAVE_FILE, 'rb') as f:
            config.PARKING_COORDINATES = pickle.load(f)

    pytesseract_engine, model_b = step0_initialize()
    cap = cv2.VideoCapture(0)
    
    app = QApplication(sys.argv)
    window = MainWindow()
    window.capture_clicked.connect(on_capture_clicked)
    window.logic_clicked.connect(on_logic_clicked)
    window.exit_clicked.connect(on_exit_clicked)
    window.show()

    timer = QTimer()
    timer.timeout.connect(lambda: process_frame(cap))
    timer.start(30)
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()