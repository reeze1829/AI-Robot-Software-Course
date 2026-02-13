import sys
import os
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QTimer
from ament_index_python.packages import get_package_share_directory

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

        if hasattr(self, 'btn_open_teleop'):
            self.btn_open_teleop.clicked.connect(self.open_teleop)

        self.teleop_window.btn_up.clicked.connect(lambda: self.send_velocity(0.2, 0.0))
        self.teleop_window.btn_down.clicked.connect(lambda: self.send_velocity(-0.2, 0.0))
        self.teleop_window.btn_left.clicked.connect(lambda: self.send_velocity(0.0, 1.0))
        self.teleop_window.btn_right.clicked.connect(lambda: self.send_velocity(0.0, -1.0))
        self.teleop_window.btn_stop.clicked.connect(lambda: self.send_velocity(0.0, 0.0))

        self.timer = QTimer()
        self.timer.timeout.connect(self.ros_spin)
        self.timer.start(10)

    def open_teleop(self):
        self.teleop_window.show()
        self.get_logger().info("수동 조종 패널이 열렸습니다!")

    def send_velocity(self, lx, az):
        msg = Twist()
        msg.linear.x = float(lx)
        msg.angular.z = float(az)
        self.cmd_vel_pub.publish(msg)
        self.get_logger().info(f"전송 -> 선속도: {lx}, 각속도: {az}")

    def ros_spin(self):
        rclpy.spin_once(self, timeout_sec=0)

def main():
    rclpy.init()
    app = QtWidgets.QApplication(sys.argv)
    node = MainNode()
    node.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
