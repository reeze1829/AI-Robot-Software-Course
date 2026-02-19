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
        self.odom_sub = self.create_subscription(
            Odometry,
            '/odom',
            self.odom_callback,
            10
        )

        self.reset_client = self.create_client(Empty, '/reset_simulation')

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
        self.is_moving_to_goal = False


        self.timer = QTimer()
        self.timer.timeout.connect(self.ros_spin)
        self.timer.start(10)

        self.btn_draw_square.clicked.connect(self.start_draw_square)
        self.square_waypoints = []
        self.current_waypoint_idx = 0
        self.is_drawing_square = False

    def open_teleop(self):
        self.teleop_window.show()
        self.get_logger().info("수동 조종 패널이 열렸습니다!")

    def move_robot(self, direction):
        if direction == "up":
            lx, az = 0.2, 0.0
            msg = "로봇이 전진합니다."
        elif direction == "down":
            lx, az = -0.2, 0.0
            msg = "로봇이 후진합니다."
        elif direction == "left":
            lx, az = 0.0, 1.0
            msg = "왼쪽으로 회전합니다."
        elif direction == "right":
            lx, az = 0.0, -1.0
            msg = "오른쪽으로 회전합니다."
        else:
            lx, az = 0.0, 0.0
            msg = "로봇이 정지했습니다."

        self.send_velocity(lx, az)
        self.text_log.append(msg)

    def send_velocity(self, lx, az):
        msg = Twist()
        msg.linear.x = float(lx)
        msg.angular.z = float(az)
        self.cmd_vel_pub.publish(msg)
        self.get_logger().info(f"전송 -> 선속도: {lx}, 각속도: {az}")

    def ros_spin(self):
        rclpy.spin_once(self, timeout_sec=0)

    def odom_callback(self, msg):
        self.curr_x = msg.pose.pose.position.x
        self.curr_y = msg.pose.pose.position.y

        q = msg.pose.pose.orientation
        siny_cosp = 2 * (q.w * q.z + q.x * q.y)
        cosy_cosp = 1 - 2 * (q.y * q.y + q.z * q.z)
        #curr_theta = math.degrees(math.atan2(siny_cosp, cosy_cosp))
        self.curr_theta = math.atan2(siny_cosp, cosy_cosp)

        #curr_linear_vel = msg.twist.twist.linear.x
        #self.lbl_pos_x.setText(f"{msg.pose.pose.position.x:.2f}")
        #self.lbl_pos_y.setText(f"{msg.pose.pose.position.y:.2f}")
        #self.lbl_theta.setText(f"{curr_theta:.1f}")
        curr_theta_deg = math.degrees(self.curr_theta)
        self.lbl_pos_x.setText(f"{self.curr_x:.2f}")
        self.lbl_pos_y.setText(f"{self.curr_y:.2f}")
        self.lbl_theta.setText(f"{curr_theta_deg:.1f}")

        if self.is_moving_to_goal:
            self.go_to_goal_logic()

    def go_to_goal_logic(self):
        dx, dy = self.target_x - self.curr_x, self.target_y - self.curr_y
        dist = math.sqrt(dx**2 + dy**2)

        if dist < 0.05:
            if self.is_drawing_square and self.current_waypoint_idx < 3:
                self.current_waypoint_idx += 1
                self.target_x, self.target_y = self.square_waypoints[self.current_waypoint_idx]
            else:
                self.is_drawing_square = False
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
        self.text_log.append("<b style='color:blue;'>[도착] 목적지에 도착했습니다!</b>")

    def btn_reset_clicked(self):
        self.get_logger().info("리셋 버튼 클릭됨!")
        self.is_moving_to_goal = False
        req = Empty.Request()
        if self.reset_client.service_is_ready():
            self.reset_client.call_async(req)
            self.text_log.append("원점 복귀 명령 전송 완료!")
        else:
            self.get_logger().error("서비스가 준비되지 않았습니다.")
            self.text_log.append("오류: 서비스 연결 실패")

    def emergency_stop(self):
        self.is_moving_to_goal = False
        self.send_velocity(0.0, 0.0)
        if hasattr(self, 'text_log'):
            self.text_log.append("<b style='color:red;'>[EMERGENCY] 긴급 정지!</b>")

    def get_distance(self):
        try:
            goal_x = float(self.input_goal_x.text())
            goal_y = float(self.input_goal_y.text())
            curr_x = float(self.lbl_pos_x.text())
            curr_y = float(self.lbl_pos_y.text())
            distance = math.sqrt((goal_x - curr_x)**2 + (goal_y - curr_y)**2)
            self.text_log.append(f"목표까지 남은 거리: {distance:.2f} m")

        except ValueError:
            pass

    def start_move_to_goal(self):
        self.target_x = float(self.input_goal_x.text())
        self.target_y = float(self.input_goal_y.text())

        self.is_moving_to_goal = True
        self.text_log.append(f"목표 ({self.target_x}, {self.target_y})로 이동!")

    def start_draw_square(self):
        self.square_waypoints = [(1.0, 0.0), (1.0, 1.0), (0.0, 1.0), (0.0, 0.0)]
        self.current_waypoint_idx = 0
        self.is_drawing_square = True
        self.target_x, self.target_y = self.square_waypoints[0]
        self.is_moving_to_goal = True


def main():
    rclpy.init()
    app = QtWidgets.QApplication(sys.argv)
    node = MainNode()
    node.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
