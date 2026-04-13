# 2차 팀 프로젝트: escortTurtlebot

다양한 환경에서 보호 대상자(VIP)를 인식하고 에스코트하는 자율주행 터틀봇 프로젝트입니다.

---

## My Core Role (핵심 역할)
**"프로젝트의 시각 지능(Visual Perception) 구현 및 모델 최적화"**

저는 팀 프로젝트에서 로봇이 주변 환경과 사람을 인식하는 '눈' 역할을 담당했습니다. 특히 실시간 처리가 중요한 로봇 환경에 맞춰 고성능 객체 인식 모델을 구축하고 최적화하는 데 집중했습니다.

### 주요 기여 사항
1. **YOLOv8 모델 학습**: 
   - 실시간 객체 감지를 위한 커스텀 데이터셋 학습 (Phone, Hands Up, Mask_VIP 등)
2. **모델 최적화 (OpenVINO)**: 
   - 학습된 모델을 인텔 CPU/GPU 환경에서 실시간으로 구동 가능하도록 최적화하여 추론 속도 향상
3. **인식 로직 이원화**: 
   - 딥러닝(YOLO)과 라이브러리(MediaPipe)의 역할을 전략적으로 배분하여 연산 효율성 극대화

---

## 상세 기술 명세 (Technical Details)
학습에 사용된 구체적인 클래스 정의, 모델 파일 구성, 인덱스 정보 등 상세한 내용은 아래 폴더의 README를 참조해 주세요.

[**YOLOv8 모델 상세 설명 보러가기 (yolo_model/README.md)**](./yolo_model/README.md)

---

## 👥 팀 정보 및 출처
* **Original Repository**: [CyCle03/escortTurtlebot](https://github.com/CyCle03/escortTurtlebot)
