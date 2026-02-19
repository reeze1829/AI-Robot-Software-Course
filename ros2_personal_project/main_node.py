import sys
import os
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QTimer
from ament_index_python.packages import get_package_share_directory
from nav_msgs.msg import Odometry
import math
from std_srvs.srv import Empty

class MainNode(Node, QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__('main_node')
        QtWidgets.QMainWindow.__init__(self)

        package_path = get_package_share_directory('ros2_personal_project')
        main_ui = os.path.join(package_path, 'ui', 'main_window.ui')
        uic.loadUi(main_ui, self)

        self.teleop_window = QtWidgets.QWidget()
        teleop_ui = os.path.join(package_path, 'ui', 'teleop_panel.ui')
        uic.loadUi(teleop_ui, self.teleop_window)

        self.cmd_vel_pub = self.create_publisher(Twist, '/cmd_vel', 10)
        self.odom_sub = self.create_subscription(Odometry, '/odom', self.odom_callback, 10)
        self.reset_client = self.create_client(Empty, '/reset_simulation')

        self.curr_x = self.curr_y = self.curr_theta = 0.0
        self.is_moving_to_goal = False
        self.is_drawing_square = False
        self.is_action_running = False
        self.current_action_idx = 0

        if hasattr(self, 'btn_open_teleop'):
            self.btn_open_teleop.clicked.connect(self.open_teleop)

        self.teleop_window.btn_up.clicked.connect(lambda: self.move_robot("up"))
        self.teleop_window.btn_down.clicked.connect(lambda: self.move_robot("down"))
        self.teleop_window.btn_left.clicked.connect(lambda: self.move_robot("left"))
        self.teleop_window.btn_right.clicked.connect(lambda: self.move_robot("right"))
        self.teleop_window.btn_stop.clicked.connect(lambda: self.move_robot("stop"))

        self.btn_reset.clicked.connect(self.btn_reset_clicked)
        self.btn_emergency_stop.clicked.connect(self.emergency_stop)
        self.btn_get_distance.clicked.connect(self.get_distance)
        self.btn_go_to_goal.clicked.connect(self.start_move_to_goal)
        self.btn_draw_square.clicked.connect(self.start_draw_square)

        if hasattr(self, 'btn_action_start'):
            self.btn_action_start.clicked.connect(self.start_action)
        if hasattr(self, 'btn_cancel_action'):
            self.btn_cancel_action.clicked.connect(self.cancel_action)

        self.timer = QTimer()
        self.timer.timeout.connect(self.ros_spin)
        self.timer.start(10)

    def open_teleop(self):
        self.teleop_window.show()

    def move_robot(self, direction):
        if direction == "up": lx, az = 0.2, 0.0
        elif direction == "down": lx, az = -0.2, 0.0
        elif direction == "left": lx, az = 0.0, 1.0
        elif direction == "right": lx, az = 0.0, -1.0
        else: lx, az = 0.0, 0.0
        self.send_velocity(lx, az)

    def send_velocity(self, lx, az):
        msg = Twist()
        msg.linear.x, msg.angular.z = float(lx), float(az)
        self.cmd_vel_pub.publish(msg)

    def ros_spin(self):
        rclpy.spin_once(self, timeout_sec=0)
        if self.is_action_running:
            self.execute_action()

    def odom_callback(self, msg):
        self.curr_x = msg.pose.pose.position.x
        self.curr_y = msg.pose.pose.position.y
        q = msg.pose.pose.orientation
        self.curr_theta = math.atan2(2*(q.w*q.z + q.x*q.y), 1 - 2*(q.y*q.y + q.z*q.z))

        self.lbl_pos_x.setText(f"{self.curr_x:.2f}")
        self.lbl_pos_y.setText(f"{self.curr_y:.2f}")
        self.lbl_theta.setText(f"{math.degrees(self.curr_theta):.1f}")

        if self.is_moving_to_goal:
            self.go_to_goal_logic()

    def go_to_goal_logic(self):
        dx, dy = self.target_x - self.curr_x, self.target_y - self.curr_y
        dist = math.sqrt(dx**2 + dy**2)
        if dist < 0.1:
            if self.is_drawing_square:
                self.current_waypoint_idx += 1
                self.progress_bar.setValue(self.current_waypoint_idx * 25)
                if self.current_waypoint_idx < 4:
                    self.target_x, self.target_y = self.square_waypoints[self.current_waypoint_idx]
                else:
                    self.is_drawing_square = False
                    self.stop_and_finish()
            else:
                self.stop_and_finish()
        else:
            err_a = math.atan2(dy, dx) - self.curr_theta
            err_a = math.atan2(math.sin(err_a), math.cos(err_a))
            lx = 0.2 if abs(err_a) < 0.1 else 0.0
            az = 0.5 * (1 if err_a > 0 else -1) if lx == 0.0 else 0.0
            self.send_velocity(lx, az)

    def stop_and_finish(self):
        self.is_moving_to_goal = False
        self.send_velocity(0.0, 0.0)
        self.text_log.append("<b style='color:blue;'>[도착] 완료!</b>")

    def start_move_to_goal(self):
        self.target_x, self.target_y = float(self.input_goal_x.text()), float(self.input_goal_y.text())
        self.is_moving_to_goal = True
        self.text_log.append(f"이동: ({self.target_x}, {self.target_y})")

    def start_draw_square(self):
        self.square_waypoints = [(1.0, 0.0), (1.0, 1.0), (0.0, 1.0), (0.0, 0.0)]
        self.current_waypoint_idx = 0
        self.is_drawing_square = True
        self.target_x, self.target_y = self.square_waypoints[0]
        self.is_moving_to_goal = True
        self.lbl_mission_status.setText("사각형 주행 중")

    def start_action(self):
        self.text_log.append("<b style='color:green;'>[Action] 주행 미션 시작!</b>")
        self.action_steps = [
            ("linear", 2.0, 0.2), ("angular", 90.0, 0.5),
            ("linear", 1.5, 0.2), ("angular", -90.0, 0.5),
            ("linear", 1.0, 0.2)
        ]
        self.current_action_idx = 0
        self.is_action_running = True
        self.prepare_next_step()

    def prepare_next_step(self):
        self.start_x, self.start_y, self.start_theta = self.curr_x, self.curr_y, self.curr_theta

    def execute_action(self):
        if not self.is_action_running: return
        step_type, target, speed = self.action_steps[self.current_action_idx]
        twist, done = Twist(), False

        if step_type == "linear":
            dist = math.sqrt((self.curr_x - self.start_x)**2 + (self.curr_y - self.start_y)**2)
            self.lbl_mission_status.setText(f"직진: {dist:.2f}/{target}m")
            if dist < target: twist.linear.x = speed
            else: done = True
        elif step_type == "angular":
            diff = math.degrees(self.curr_theta - self.start_theta)
            while diff > 180: diff -= 360
            while diff < -180: diff += 360
            self.lbl_mission_status.setText(f"회전: {abs(diff):.1f}/{abs(target)}°")
            if abs(diff) < abs(target): twist.angular.z = -speed if target > 0 else speed
            else: done = True

        self.cmd_vel_pub.publish(twist)
        if done:
            self.send_velocity(0.0, 0.0)
            self.current_action_idx += 1
            if self.current_action_idx < len(self.action_steps): self.prepare_next_step()
            else:
                self.is_action_running = False
                self.lbl_mission_status.setText("미션 완료")
                self.text_log.append("<b style='color:blue;'>[Result] 모든 경로 주행 성공!</b>")

    def cancel_action(self):
        self.is_action_running = False
        self.send_velocity(0.0, 0.0)
        self.lbl_mission_status.setText("미션 종료")
        self.text_log.append("<b style='color:orange;'> 사용자가 미션을 취소했습니다.</b>")

    def btn_reset_clicked(self):
        if self.reset_client.service_is_ready():
            self.reset_client.call_async(Empty.Request())
            self.text_log.append("원점 리셋 완료")

    def emergency_stop(self):
        self.is_moving_to_goal = self.is_action_running = False
        self.send_velocity(0.0, 0.0)
        self.text_log.append("<b style='color:red;'>[EMERGENCY] 긴급 정지!</b>")

    def get_distance(self):
        try:
            gx, gy = float(self.input_goal_x.text()), float(self.input_goal_y.text())
            d = math.sqrt((gx - self.curr_x)**2 + (gy - self.curr_y)**2)
            self.text_log.append(f"거리: {d:.2f} m")
        except: pass

def main():
    rclpy.init()
    app = QtWidgets.QApplication(sys.argv)
    node = MainNode()
    node.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
