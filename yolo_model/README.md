# 🐢 Escort Turtlebot YOLO Models

This directory contains the YOLOv8 models used as the 'eyes' of the leader-follower robot project, specifically trained to detect people and their states.

**Note on Gesture Recognition:** Gesture recognition (e.g., counting fingers) is NOT handled by these YOLO models. It is performed by the `escort_vision_node` using the `mediapipe` library.

## 📌 Model Overview
The models are designed to facilitate interaction between humans and TurtleBots by identifying VIP status, safety gear, and specific objects.

## 🏷️ Class Definitions

### `last.pt` (Final Model)
Use these class indices when parsing `results.box.cls` from `last.pt`:

| Index | Class Name | Description |
| :--- | :--- | :--- |
| **0** | **Phone** | Person holding or using a smartphone. |
| **1** | **Hands Up** | Hand gesture (e.g., for signaling the robot). |
| **2** | **Mask VIP** | Identified VIP user wearing a mask. |

### `best.pt` (Initial Mask Detection Model)
This model has 3 classes for mask detection:
- `with_mask`
- `without_mask`
- `mask_weared_incorrect` (Note: the model output class is `incorrect`, but the code uses `mask_weared_incorrect` for display)

## 🛠️ Artifacts & Models
- `best.pt`: Initial training weights for mask detection.
- `last.pt`: Final comprehensive model (Phone, HandsUp, Mask_VIP).
- `last_openvino_model/`: Optimized version of `last.pt` for Intel hardware.

---

# 한국어 안내

이 디렉터리는 에스코트 터틀봇 프로젝트의 시각 인식을 담당하는 YOLOv8 모델을 포함합니다. 이 모델은 로봇 주변의 사람을 감지하고, 상태(VIP 여부, 기기 사용 등)를 파악하기 위해 학습되었습니다.

**참고: 제스처 인식** 제스처 인식(예: 손가락 개수 세기)은 YOLO 모델이 아닌 `escort_vision_node`에서 `mediapipe` 라이브러리를 통해 처리됩니다.

## 📌 주요 클래스 정의

### `last.pt` (최종 모델)
`last.pt` 모델의 `result.box.cls`로 반환되는 인덱스 및 상세 설명입니다:

| 인덱스 | 클래스명 | 설명 |
| :--- | :--- | :--- |
| **0** | **Phone** | 스마트폰을 손에 들고 있거나 사용 중인 상태. |
| **1** | **Hands Up** | 손을 머리 위로 든 상태 (로봇 호출 등의 제스처). |
| **2** | **Mask VIP** | 마스크를 착용한 보호 대상자(VIP). |

### `best.pt` (초기 마스크 인식 모델)
마스크 착용 여부를 판별하는 모델이며, 3개의 클래스를 가집니다:
- `with_mask`
- `without_mask`
- `mask_weared_incorrect` (참고: 모델의 실제 출력 클래스는 `incorrect` 이지만, 코드에서는 `mask_weared_incorrect` 라는 이름으로 사용됩니다.)

## 🛠️ 포함된 모델 파일
- `last.pt`: Phone, HandsUp, Mask_VIP를 모두 포함하는 최종 통합 학습 모델.
- `last_openvino_model/`: `last.pt`를 인텔 CPU/GPU 환경에 최적화한 OpenVINO 형식 모델.
- `best.pt`: 초기 단계의 마스크 착용 여부 판별 모델.
