# escort_follower

C++ package for the follower robot.

This package contains the core algorithms for the follower robot to track the leader. It calculates the leader's position and generates a hybrid tracking path.

## How to Build

This package is part of the `controllserver` workspace. Build the entire workspace from the root directory (`~/escort_ws`):

```bash
cd ~/escort_ws
colcon build --packages-up-to escort_follower
source install/setup.bash
```

## How to Run

Use the launch files in `escort_turtlebot_pkg` to run the system.
