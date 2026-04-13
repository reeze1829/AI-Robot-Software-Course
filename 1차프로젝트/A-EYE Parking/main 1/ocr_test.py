import cv2
import pytesseract
import numpy as np
import re
from PIL import ImageFont, ImageDraw, Image

# 1. 경로 설정
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
font_path = "C:/Windows/Fonts/malgun.ttf"
font = ImageFont.truetype(font_path, 30)

def draw_korean_text(img, text, position, font, color):
    img_pil = Image.fromarray(img)
    draw = ImageDraw.Draw(img_pil)
    draw.text(position, text, font=font, fill=color)
    return np.array(img_pil)

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

while True:
    ret, frame = cap.read()
    if not ret: break

    display_frame = cv2.flip(frame, 1) # 거울 모드

    # [영역 설정] 하단 컴팩트 사이즈
    roi_w, roi_h = 320, 70
    roi_x, roi_y = 160, 370

    # 인식용 ROI 추출
    roi = frame[roi_y:roi_y + roi_h, roi_x:roi_x + roi_w]

    # [전처리] 이진화 및 확대
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    gray = cv2.resize(gray, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # [OCR 인식 및 필터링]
    raw_text = pytesseract.image_to_string(thresh, lang='kor+eng', config='--psm 6').strip()

    # 한글과 숫자만 남기기 (특수문자 제거)
    clean_text = re.sub(r'[^가-힣0-9]', '', raw_text)

    # UI 출력 위치 계산
    mirror_x = 640 - roi_x - roi_w
    cv2.rectangle(display_frame, (mirror_x, roi_y), (mirror_x + roi_w, roi_y + roi_h), (0, 255, 0), 2)

    # [핵심 수정] 7글자 이상(번호판 형식)일 때만 화면에 표시
    # 공백을 제외한 글자 수가 7개 이상인지 확인
    if len(clean_text) >= 7:
        # 결과 배경창
        cv2.rectangle(display_frame, (mirror_x, roi_y - 45), (mirror_x + roi_w, roi_y), (0, 0, 0), -1)
        # 결과 텍스트 출력
        display_frame = draw_korean_text(display_frame, f" {clean_text}", (mirror_x + 5, roi_y - 40), font, (255, 255, 255))

    # 화면 표시
    cv2.imshow("Number Plate Filter Mode", display_frame)
    cv2.imshow("AI Vision (Check Focus)", thresh)

    if cv2.waitKey(1) & 0xFF == ord('q'): break

cap.release()
cv2.destroyAllWindows()
