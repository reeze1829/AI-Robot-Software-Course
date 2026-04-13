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


def get_ocr_result(frame):
    # [영역 설정]
    roi_w, roi_h = 420, 100
    roi_x, roi_y = 110, 220

    # 예외 처리: 프레임이 영역보다 작을 경우 방지
    try:
        roi = frame[roi_y:roi_y + roi_h, roi_x:roi_x + roi_w]

        # 1. Grayscale
        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        # 2. Resize
        gray = cv2.resize(gray, None, fx=3, fy=3, interpolation=cv2.INTER_CUBIC)
        # 3. Gaussian Blur
        blur = cv2.GaussianBlur(gray, (3, 3), 0)
        # 4. OTSU Thresholding
        _, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        # [디버깅 코드 추가] 모델이 실제로 자른 이미지를 윈도우로 띄워봅니다.
        # 이 창에 번호판이 깨끗하게 나오고 있는지 확인하세요.
        cv2.imshow("OCR_INPUT_CHECK", thresh)

        # [OCR 인식 및 필터링]
        raw_text = pytesseract.image_to_string(thresh, lang='kor+eng', config='--psm 7').strip()
        clean_text = re.sub(r'[^가-힣0-9]', '', raw_text)

        return clean_text, thresh
    except:
        return "", None


if __name__ == '__main__':
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # 변수명 오타 수정: processed_ing -> processed_img
        text, processed_img = get_ocr_result(frame)
        display_frame = cv2.flip(frame, 1)  # 거울 모드

        # 들여쓰기 수정
        if text:
            display_frame = draw_korean_text(display_frame, text, (10, 50), font, (0, 255, 0))

        # 화면 표시 (if text 블록 밖으로 꺼내야 텍스트가 없어도 화면이 보입니다)
        cv2.imshow("Test Mode", display_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()