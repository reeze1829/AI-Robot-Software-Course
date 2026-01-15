import cv2
import numpy as np
import os

# 1. 폴더 생성 범위를 0~9로 확장
base_path = "digit_data"
for i in range(10): # 0부터 9까지 폴더 생성
    os.makedirs(f"{base_path}/{i}", exist_ok=True)

cap = cv2.VideoCapture(0)
print("수집 시작: 키보드의 0~9 숫자를 누르면 해당 폴더에 저장됩니다. (ESC: 종료)")

while True:
    ret, frame = cap.read()
    if not ret: break

    flip_frame = cv2.flip(frame, 1)
    height, width, _ = frame.shape
    center_x, center_y = width // 2, height // 2

    roi = flip_frame[center_y - 150:center_y + 150, center_x - 150:center_x + 150]
    cv2.rectangle(flip_frame, (center_x - 150, center_y - 150), (center_x + 150, center_y + 150), (0, 0, 255), 2)

    cv2.imshow("Webcam", flip_frame)

    key = cv2.waitKey(1) & 0xFF

    # 2. 키보드 입력 범위를 0~9로 수정
    if ord('0') <= key <= ord('9'):
        digit = chr(key) # 누른 숫자 키를 문자로 변환 ('0'~'9')

        # --- [전처리 로직] ---
        gray_image = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        gaussian_blur = cv2.GaussianBlur(gray_image, (5, 5), 3)
        _, otsu_thread = cv2.threshold(gaussian_blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        kernel = np.ones((5, 5), np.uint8)
        erosion = cv2.erode(otsu_thread, kernel, iterations=1)
        reversed_img = cv2.bitwise_not(erosion)

        # 방향 교정 (거울 모드 해제)
        corrected_img = cv2.flip(reversed_img, 1)

        # NumPy 테두리 제거 (노이즈 방지)
        corrected_img[0:5, :] = 0; corrected_img[-5:, :] = 0
        corrected_img[:, 0:5] = 0; corrected_img[:, -5:] = 0

        # --- [저장 및 확인] ---
        save_dir = f"{base_path}/{digit}"
        file_count = len(os.listdir(save_dir))
        file_path = os.path.join(save_dir, f"{digit}_{file_count}.png")

        # 28x28 리사이즈 후 저장
        final_save = cv2.resize(corrected_img, (28, 28), interpolation=cv2.INTER_AREA)
        cv2.imwrite(file_path, final_save)

        print(f"[{digit}] 폴더에 저장 완료! (현재 {file_count + 1}장)")

    elif key == 27: # ESC 종료
        break

cap.release()
cv2.destroyAllWindows()
