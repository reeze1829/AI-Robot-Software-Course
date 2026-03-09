import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Point
from nav_msgs.msg import Odometry
import math

class LeaderNode(Node):
    def __init__(self):
        super().__init__('leader_node')
        # 토픽 리스트와 일치함
        self.create_subscription(Odometry, '/leader/odom', self.odom_callback, 10)
        self.pos_pub = self.create_publisher(Point, '/leader/relative_pos', 10)
        self.get_logger().info('Leader Node가 작동 중입니다...')

    def odom_callback(self, msg):
        x = msg.pose.pose.position.x
        y = msg.pose.pose.position.y
        q = msg.pose.pose.orientation
        yaw = math.atan2(2*(q.w*q.z + q.x*q.y), 1-2*(q.y*q.y + q.z*q.z))
        
        target = Point()
        target.x = x - 1.0 * math.cos(yaw) # 1m 뒤
        target.y = y - 1.0 * math.sin(yaw)
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