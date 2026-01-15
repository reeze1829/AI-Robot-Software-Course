import cv2
import numpy as np
import tensorflow as tf
import pandas as pd
from datetime import datetime
import os
from PIL import ImageFont, ImageDraw, Image

# 1. 한글 출력 함수
def draw_korean(img, text, pos, size, color):
    img_pil = Image.fromarray(img)
    draw = ImageDraw.Draw(img_pil)
    try:
        font = ImageFont.truetype("malgun.ttf", size)
    except:
        font = ImageFont.load_default()
    draw.text(pos, text, font=font, fill=color)
    return np.array(img_pil)

# 2. 모델 및 기본 설정
model = tf.keras.models.load_model("digit_model.h5")
parking_db = {"0128": "지하 3층 - A5", "3597": "지하 2층 - E3"}
label_map = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

cap = cv2.VideoCapture(0)
w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# 3. 영상 저장 설정
fourcc = cv2.VideoWriter_fourcc('X', 'V', 'I', 'D')
out = cv2.VideoWriter('parking_record.avi', fourcc, 20.0, (w, h))

# 4. 상태 관리 변수
input_list = []
log_list = []
display_timer = 0
active_target = ""
# [수정 포인트 1: 초기 시작 메시지]
action_msg = "숫자 영상인식을 활용한 주차 위치 확인 시스템입니다. "
action_timer = 60

while True:
    ret, frame = cap.read()
    if not ret: break
    frame = cv2.flip(frame, 1)

    # --- UI 그리기 (왼쪽 대시보드) ---
    startX, width, rect_h = 5, 140, 50
    c1 = (150, 150, 255) if active_target == "0128" and (display_timer // 10) % 2 == 0 else (60,60,60)
    cv2.rectangle(frame, (startX, 100), (startX+width, 150), c1, -1)
    cv2.putText(frame, "0128", (startX+35, 135), cv2.FONT_HERSHEY_DUPLEX, 0.7, (255,255,255), 1)

    c2 = (150, 150, 255) if active_target == "3597" and (display_timer // 10) % 2 == 0 else (60,60,60)
    cv2.rectangle(frame, (startX, 155), (startX+width, 205), c2, -1)
    cv2.putText(frame, "3597", (startX+35, 190), cv2.FONT_HERSHEY_DUPLEX, 0.7, (255,255,255), 1)

    # --- 중앙 ROI ---
    x1, y1, x2, y2 = w//2-150, h//2-150, w//2+150, h//2+150
    roi = frame[y1:y2, x1:x2]
    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)

    cv2.putText(frame, f"INPUT: {input_list}", (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)

    # --- 행동 자막 출력 ---
    if action_timer > 0:
        cv2.rectangle(frame, (0, h-60), (w, h), (0,0,0), -1)
        frame = draw_korean(frame, action_msg, (20, h-45), 22, (255, 255, 255))
        action_timer -= 1

    # 주차 위치 기호 표시
    if active_target in parking_db and display_timer > 0:
        frame = draw_korean(frame, parking_db[active_target], (startX+width+10, 115 if active_target=="0128" else 170), 25, (0,255,0))
        display_timer -= 1

    out.write(frame)
    cv2.imshow("Smart Parking", frame)

    key = cv2.waitKey(1) & 0xFF

    # --- 제어 로직 ---
    if key == ord('c') or key == ord('C'):
        # [수정 포인트 2: C키를 눌렀을 때 (분석 시작)]
        action_msg = "번호를 판독하고 있습니다."
        action_timer = 30

        # 전처리 및 분석
        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 3)
        _, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        img = cv2.bitwise_not(cv2.flip(cv2.erode(thresh, np.ones((5, 5), np.uint8)), 1))
        img[0:15, :], img[-15:, :], img[:, 0:15], img[:, -15:] = 0, 0, 0, 0

        test_img = cv2.resize(img, (28, 28)).reshape(1, 28, 28, 1) / 255.0

        pred = model.predict(test_img, verbose=0)

        if np.max(pred) > 0.98:
            res = label_map[np.argmax(pred)]
            input_list.append(res)
            # [수정 포인트 3: 숫자 하나 인식 성공했을 때]
            action_msg = f"숫자'{res}' 을 인식 완료했습니다."
            action_timer = 40

            if len(input_list) == 4:
                car_num = "".join(map(str, input_list))
                now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                if car_num in parking_db:
                    active_target, display_timer = car_num, 90
                    # [수정 포인트 4: 4자리 모두 맞아서 위치를 찾았을 때]
                    action_msg = f" {car_num} 현재 주차위치가 화면에 표시됩니다. {parking_db[car_num]}"
                    log_list.append({"Time": now, "CarNum": car_num, "Loc": parking_db[car_num], "Status": "SUCCESS"})
                else:
                    # [수정 포인트 5: 4자리 입력했는데 등록 안 된 번호일 때]
                    action_msg = " 등록이 안된 번호일 경우 다시 한번 시도를 해야 합니다."
                    log_list.append({"Time": now, "CarNum": car_num, "Loc": "None", "Status": "NOT_FOUND"})
                input_list = []
                action_timer = 100
        else:
            # [수정 포인트 6: 인식이 잘 안 됐을 때]
            action_msg = "인식이 잘 되지 않은 경우에도 다시 한번 시도 해야 합니다."
            action_timer = 40

    elif key == ord('r') or key == ord('R'):
        input_list, active_target, display_timer = [], "", 0
        # [수정 포인트 7: 리셋(R) 키 눌렀을 때]
        action_msg = "'R(r)'키를 누르면 다시 시작할 수 있습니다. "
        action_timer = 50

    elif key == 27: break

cap.release()
out.release()
cv2.destroyAllWindows()

# 판다스 저장
if log_list:
    df = pd.DataFrame(log_list)
    df.to_csv("parking_access_log.csv",
              index=False,
              encoding='utf-8-sig',
              mode='a',
              header=not os.path.exists("parking_access_log.csv"))
