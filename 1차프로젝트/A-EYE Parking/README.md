# 1차 프로젝트: A-EYE Parking
**OpenCV와 Tesseract를 활용한 지능형 주차 안내 시스템**

---

## My Role: Core Logic & Environment Mapping
본 프로젝트에서 차량 인식을 위한 **비전 파이프라인** 구축과 로봇 주행의 기초가 되는 **주차장 지도 작성(SLAM)**을 담당했습니다.

### 주요 성과
- **OCR 인식 파이프라인 구축**: 이미지 전처리 및 정규표현식 검증을 통해 번호판 인식의 신뢰도 확보.
- **SLAM 기반 주차장 맵 데이터 생성**: Lidar 센서를 활용하여 로봇이 주행할 실제 주차장 환경을 2D 지도로 디지털화함.
- **맞춤형 안내 로직 설계**: DB의 사용자 데이터와 실시간 주차 상태를 결합한 의사결정 프로세스 구현.

---

## 주요 구현 기술 설명

### 1. OCR 인식률 최적화 및 정규표현식 검증
Tesseract 엔진의 정확도를 높이기 위해 OpenCV 전처리를 수행하고, 정규표현식을 통해 유효한 데이터만 추출했습니다.

```python
# [이미지 전처리] Grayscale -> 3배 확대 -> Gaussian Blur -> OTSU 이진화
gray = cv2.cvtColor(roi_frame, cv2.COLOR_BGR2GRAY)
gray = cv2.resize(gray, None, fx=3, fy=3, interpolation=cv2.INTER_CUBIC)
blur = cv2.GaussianBlur(gray, (3, 3), 0)
_, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

# [데이터 검증] 한국 번호판 규격(숫자 2~3자리 + 한글 + 숫자 4자리) 필터링
clean_text = re.sub(r'[^가-힣0-9]', '', raw_text) # 특수문자 제거
match = re.search(r'\d{2,3}[가-힣]\d{4}', clean_text) # 규격 매칭
