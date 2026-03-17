# escort_turtlebot_pkg

Python package for launch/bridge integration.

This package is responsible for:
- Launching the simulation environment.
- Managing launch files for the entire system.
- Bridging TF between the robots.
- Vision processing for gesture recognition and mask detection.
- A GUI for system monitoring.

## How to Build

This package is part of the `controllserver` workspace. Build the entire workspace from the root directory (`~/escort_ws`):

```bash
cd ~/escort_ws
colcon build --packages-up-to escort_turtlebot_pkg
source install/setup.bash
```

## How to Run

This package contains the main launch file to start the system:

```bash
ros2 launch escort_turtlebot_pkg escort_full_system.launch.py
```
