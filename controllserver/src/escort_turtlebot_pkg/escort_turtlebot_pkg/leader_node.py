import math

import rclpy
from geometry_msgs.msg import Point
from nav_msgs.msg import Odometry
from rclpy.node import Node


class LeaderNode(Node):
    def __init__(self):
        super().__init__('leader_node')
        self.declare_parameter('leader_odom_topic', '/TB3_1/odom')
        self.declare_parameter('target_topic', '/leader/relative_pos')
        self.declare_parameter('follow_offset', 1.0)

        odom_topic = self.get_parameter('leader_odom_topic').get_parameter_value().string_value
        target_topic = self.get_parameter('target_topic').get_parameter_value().string_value
        self.follow_offset = self.get_parameter('follow_offset').get_parameter_value().double_value

        self.create_subscription(Odometry, odom_topic, self.odom_callback, 10)
        self.pos_pub = self.create_publisher(Point, target_topic, 10)
        self.get_logger().info(
            f'Leader node started (odom: {odom_topic}, target: {target_topic}, offset: {self.follow_offset:.2f}m)'
        )

    def odom_callback(self, msg: Odometry):
        x = msg.pose.pose.position.x
        y = msg.pose.pose.position.y
        q = msg.pose.pose.orientation
        yaw = math.atan2(2 * (q.w * q.z + q.x * q.y), 1 - 2 * (q.y * q.y + q.z * q.z))

        target = Point()
        target.x = x - self.follow_offset * math.cos(yaw)
        target.y = y - self.follow_offset * math.sin(yaw)
        self.pos_pub.publish(target)


def main(args=None):
    rclpy.init(args=args)
    node = LeaderNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
