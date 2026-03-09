import rclpy
from geometry_msgs.msg import Twist
from rclpy.node import Node


class LeaderInitialMoveNode(Node):
    def __init__(self):
        super().__init__('leader_initial_move_node')
        self.declare_parameter('cmd_vel_topic', '/TB3_1/cmd_vel')
        self.declare_parameter('distance', 0.5)
        self.declare_parameter('speed', 0.10)
        self.declare_parameter('startup_delay_sec', 2.0)

        cmd_vel_topic = self.get_parameter('cmd_vel_topic').get_parameter_value().string_value
        distance = self.get_parameter('distance').get_parameter_value().double_value
        speed = self.get_parameter('speed').get_parameter_value().double_value
        startup_delay_sec = self.get_parameter('startup_delay_sec').get_parameter_value().double_value

        self.speed = max(0.01, abs(speed))
        self.move_duration = max(0.0, abs(distance) / self.speed)
        self.direction = 1.0 if distance >= 0.0 else -1.0
        self.active = False
        self.elapsed = 0.0

        self.cmd_pub = self.create_publisher(Twist, cmd_vel_topic, 10)

        self.timer_period = 0.05
        self.control_timer = self.create_timer(self.timer_period, self._control_loop)
        self.start_timer = self.create_timer(startup_delay_sec, self._start_move)

    def _start_move(self):
        self.start_timer.cancel()
        self.active = True
        self.elapsed = 0.0

    def _control_loop(self):
        twist = Twist()
        if self.active and self.elapsed < self.move_duration:
            twist.linear.x = self.direction * self.speed
            self.elapsed += self.timer_period
        else:
            self.active = False
            self.control_timer.cancel()
        self.cmd_pub.publish(twist)


def main(args=None):
    rclpy.init(args=args)
    node = LeaderInitialMoveNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.cmd_pub.publish(Twist())
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
