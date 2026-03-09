# escort_turtlebot_pkg

Python launch/bridge integration package for escort simulation and runtime orchestration.

## What It Does
- Launches multi-TurtleBot simulation (`escort_sim.launch.py`).
- Spawns robots with namespaced frames (`TB3_1`, `TB3_2`).
- Runs a hybrid follower behavior:
  - Leader rear-target idea from `team_project`
  - Nav2 `FollowPath` execution from `escort_follower`

## Build
```bash
cd ~/escort_ws/controllserver
colcon build --packages-select escort_turtlebot_pkg
source install/setup.bash
```

## Integrated Simulation
```bash
cd ~/escort_ws/controllserver
source /opt/ros/humble/setup.bash
source ~/turtlebot3_ws/install/setup.bash
source install/setup.bash

ros2 launch escort_turtlebot_pkg escort_sim.launch.py
```

## Main Launch Arguments (`escort_sim.launch.py`)
- `use_sim_time` (bool, default: `true`)
  Use simulation clock.
- `leader_x`, `leader_y` (double)
  Leader spawn pose.
- `follower_x`, `follower_y` (double)
  Follower spawn pose.

## 한국어 안내

이 패키지는 에스코트 시뮬레이션 실행을 통합하는 Python launch/bridge 패키지입니다.

### 주요 기능
- 멀티 터틀봇 시뮬레이션 실행 (`escort_sim.launch.py`)
- 네임스페이스 기반 프레임(`TB3_1`, `TB3_2`)으로 로봇 스폰
- 하이브리드 추종 방식 사용
  - `team_project`의 리더 후방 목표점 아이디어
  - `escort_follower`의 Nav2 `FollowPath` 추종 실행

### 빌드
```bash
cd ~/escort_ws/controllserver
colcon build --packages-select escort_turtlebot_pkg
source install/setup.bash
```

### 통합 시뮬레이션 실행
```bash
cd ~/escort_ws/controllserver
source /opt/ros/humble/setup.bash
source ~/turtlebot3_ws/install/setup.bash
source install/setup.bash

ros2 launch escort_turtlebot_pkg escort_sim.launch.py
```

### 주요 런치 인자 (`escort_sim.launch.py`)
- `use_sim_time` (기본값 `true`): 시뮬레이션 시간 사용 여부
- `leader_x`, `leader_y`: leader 스폰 위치
- `follower_x`, `follower_y`: follower 스폰 위치
