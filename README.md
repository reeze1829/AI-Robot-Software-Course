# escortTurtlebot

Shared ROS 2 workspace for multi-member TurtleBot projects focusing on leader-follower orchestration, SLAM integration, and autonomous navigation.

## Key Features
- **Hybrid Leader-Follower**: Combines virtual target projection with Nav2 paths.
- **ICP-based TF Alignment**: Real-time synchronization of multi-robot coordinate frames using LiDAR scan matching.
- **Robust SLAM**: Enhanced stability filters to protect map integrity during tracking.
- **Integrated Safety**: Ultrasonic emergency stop and recovery behaviors.

## Repository Guide
- Root `README.md` contains project-wide conventions and package index.
- Each package should keep its own detailed README for build/run/config.

## Package Index
- `controllserver/src/escort_follower`
  C++ follower node package.
  See module docs: `controllserver/src/escort_follower/README.md`
- `controllserver/src/escort_turtlebot_pkg`
  Python launch/bridge integration package.
  See module docs: `controllserver/src/escort_turtlebot_pkg/README.md`

## Common Build (Workspace)
```bash
cd ~/escort_ws/controllserver
colcon build
source install/setup.bash
```

---

## 한국어 안내

이 워크스페이스는 터틀봇3를 이용한 리더-팔로워 주행, SLAM 통합 및 자율 주행 프로토타입을 포함하는 다중 로봇 협업 프로젝트 저장소입니다.

### 주요 기능
- **하이브리드 리더-팔로워**: 리더의 후방에 가상 타겟을 생성하고 Nav2 경로를 통해 추종하는 방식의 결합
- **ICP 기반 TF 정렬**: LiDAR 스캔 데이터를 정합하여 리더와 팔로워 간의 실시간 좌표계를 동기화
- **강인한 SLAM**: 주행 중 맵 오염 및 흔들림을 방지하기 위한 이동 기반 필터링 및 안정화 알고리즘 적용
- **통합 안전 시스템**: 초음파 센서를 이용한 긴급 정지 및 데이터 소실 시 마지막 위치 대기 복구 행동

### 리포지토리 가이드
- 루트 `README.md`: 프로젝트 전체 규칙, 패키지 목록 및 공통 빌드 방법 안내
- 각 패키지 README: 개별 모듈의 상세 실행 방법, 파라미터 및 토픽/TF 정보 제공

### 패키지 목록 (Package Index)
- **`controllserver/src/escort_follower`** (C++ 패키지)
  - 리더의 위치를 계산하고 하이브리드 추종 경로를 생성하는 핵심 알고리즘 패키지입니다.
  - 상세 문서: [escort_follower/README.md](file:///home/penguin/escort_ws/controllserver/src/escort_follower/README.md)
- **`controllserver/src/escort_turtlebot_pkg`** (Python 패키지)
  - 시뮬레이션 환경 구축, 런치 파일 관리 및 로봇 간의 TF 브리지를 총괄하는 통합 패키지입니다.
  - 상세 문서: [escort_turtlebot_pkg/README.md](file:///home/penguin/escort_ws/controllserver/src/escort_turtlebot_pkg/README.md)

### 공통 빌드 (Common Build)
워크스페이스 프로젝트 전체를 빌드하고 환경을 설정하는 방법입니다:
```bash
cd ~/escort_ws/controllserver
colcon build
source install/setup.bash
```
