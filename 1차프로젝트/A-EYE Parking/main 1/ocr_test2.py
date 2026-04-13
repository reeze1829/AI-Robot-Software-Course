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

    # [영역 설정]
    roi_w, roi_h = 320, 70
    roi_x, roi_y = 160, 370
    roi = frame[roi_y:roi_y + roi_h, roi_x:roi_x + roi_w]

    # Grayscale: 흑백으로 전환
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

    # Resize: 3배 확대
    gray = cv2.resize(gray, None, fx=3, fy=3, interpolation=cv2.INTER_CUBIC)

    # Gaussian Blur: (3, 3) 커널로 미세 노이즈 제거
    blur = cv2.GaussianBlur(gray, (3, 3), 0)

    # OTSU Thresholding: 이진화 (흑백 대비 극대화)
    _, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)


    # [OCR 인식 및 필터링]
    raw_text = pytesseract.image_to_string(thresh, lang='kor+eng', config='--psm 7').strip()
    clean_text = re.sub(r'[^가-힣0-9]', '', raw_text)

    # UI 출력 및 미러링 계산
    mirror_x = 640 - roi_x - roi_w
    cv2.rectangle(display_frame, (mirror_x, roi_y), (mirror_x + roi_w, roi_y + roi_h), (0, 255, 0), 2)

    if len(clean_text) >= 7:
        cv2.rectangle(display_frame, (mirror_x, roi_y - 45), (mirror_x + roi_w, roi_y), (0, 0, 0), -1)
        display_frame = draw_korean_text(display_frame, f" {clean_text}", (mirror_x + 5, roi_y - 40), font, (255, 255, 255))

    # 화면 표시
    cv2.imshow("Number Plate Filter Mode", display_frame)
    cv2.imshow("AI Vision (Clean Image)", thresh) # 전처리된 결과 확인용

    if cv2.waitKey(1) & 0xFF == ord('q'): break

cap.release()
cv2.destroyAllWindows()