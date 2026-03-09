import math

import rclpy
from geometry_msgs.msg import Point
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from rclpy.node import Node


class FollowerNode(Node):
    def __init__(self):
        super().__init__('follower_node')
        self.declare_parameter('follower_odom_topic', '/TB3_2/odom')
        self.declare_parameter('target_topic', '/leader/relative_pos')
        self.declare_parameter('cmd_vel_topic', '/TB3_2/cmd_vel')
        self.declare_parameter('stop_distance', 0.1)
        self.declare_parameter('linear_gain', 0.5)
        self.declare_parameter('angular_gain', 1.5)
        self.declare_parameter('max_linear', 0.22)

        odom_topic = self.get_parameter('follower_odom_topic').get_parameter_value().string_value
        target_topic = self.get_parameter('target_topic').get_parameter_value().string_value
        cmd_vel_topic = self.get_parameter('cmd_vel_topic').get_parameter_value().string_value

        self.stop_distance = self.get_parameter('stop_distance').get_parameter_value().double_value
        self.linear_gain = self.get_parameter('linear_gain').get_parameter_value().double_value
        self.angular_gain = self.get_parameter('angular_gain').get_parameter_value().double_value
        self.max_linear = self.get_parameter('max_linear').get_parameter_value().double_value

        self.cmd_pub = self.create_publisher(Twist, cmd_vel_topic, 10)
        self.create_subscription(Odometry, odom_topic, self.odom_callback, 10)
        self.create_subscription(Point, target_topic, self.target_callback, 10)

        self.curr_x = 0.0
        self.curr_y = 0.0
        self.curr_yaw = 0.0
        self.get_logger().info(
            f'Follower node started (odom: {odom_topic}, target: {target_topic}, cmd_vel: {cmd_vel_topic})'
        )

    def odom_callback(self, msg: Odometry):
        self.curr_x = msg.pose.pose.position.x
        self.curr_y = msg.pose.pose.position.y
        q = msg.pose.pose.orientation
        self.curr_yaw = math.atan2(2 * (q.w * q.z + q.x * q.y), 1 - 2 * (q.y * q.y + q.z * q.z))

    def target_callback(self, msg: Point):
        dx = msg.x - self.curr_x
        dy = msg.y - self.curr_y
        dist = math.sqrt(dx * dx + dy * dy)
        angle_to_target = math.atan2(dy, dx)
        angle_error = math.atan2(
            math.sin(angle_to_target - self.curr_yaw),
            math.cos(angle_to_target - self.curr_yaw),
        )

        twist = Twist()
        if dist > self.stop_distance:
            twist.linear.x = min(self.linear_gain * dist, self.max_linear)
            twist.angular.z = self.angular_gain * angle_error
        self.cmd_pub.publish(twist)


def main(args=None):
    rclpy.init(args=args)
    node = FollowerNode()
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
