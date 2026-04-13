import cv2
import pytesseract
import re

def step1_ocr_process(roi_frame):                         
    # Grayscale: 흑백 전환
    gray = cv2.cvtColor(roi_frame, cv2.COLOR_BGR2GRAY)

    # Resize: 3배 확대
    gray = cv2.resize(gray, None, fx=3, fy=3, interpolation=cv2.INTER_CUBIC)

    # Gaussian Blur: (3, 3)커널로 노이즈 제거
    blur = cv2.GaussianBlur(gray, (3, 3), 0)

    # OTSU Thresholding: 이진화
    _, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # 전처리 이미지 확인
    cv2.imshow("AI Vision (Clean Image)", thresh)

    # Tesseract 분석
    raw_text = pytesseract.image_to_string(thresh, lang='kor+eng', config='--psm 7').strip()

    # 한글과 숫자만 남기기 (마지막 코드의 정규식)
    clean_text = re.sub(r'[^가-힣0-9]', '', raw_text)

    match = re.search(r'\d{2,3}[가-힣]\d{4}', clean_text)

    if match:
        clean_text = match.group()
    else:
        clean_text = clean_text[:8]
    return clean_text

def on_capture_clicked():
    global current_frame, recognized_vehicle_no
    
    # 영상 프레임이 있으면 OCR 돌려서 번호판 텍스트 추출
    if current_frame is not None:
        recognized_vehicle_no = step1_ocr_process(current_frame)

        # 한글이 포함되어 있는지 확인
        is_real_plate = re.search(r'[가-힣]', recognized_vehicle_no)
        
        # '가1234' 같이 한글 뒤에 숫자 4자리까지만 허용  
        is_valid_format = re.search(r'[가-힣]\d{4}$', recognized_vehicle_no)
        
        # 전체 글자 수가 7~8자인지 확인
        is_correct_length = 7 <= len(recognized_vehicle_no) <= 8
        
        # 위 조건들을 다 만족하면 유효한 번호판으로 판단
        if is_real_plate and is_valid_format and is_correct_length:
            user_data = step2_db_check(recognized_vehicle_no)
            window.update_message(f"인식 성공: {recognized_vehicle_no}")
            if user_data:
                print(f"로그: {user_data['name']}님 확인")
        else:
            window.update_message(f"인식 중... ({recognized_vehicle_no})")


