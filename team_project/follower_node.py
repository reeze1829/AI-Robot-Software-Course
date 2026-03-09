import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist, Point
from nav_msgs.msg import Odometry
import math

class FollowerNode(Node):
    def __init__(self):
        super().__init__('follower_node')
        self.cmd_pub = self.create_publisher(Twist, '/follower/cmd_vel', 10)
        self.create_subscription(Odometry, '/follower/odom', self.odom_callback, 10)
        self.create_subscription(Point, '/leader/relative_pos', self.target_callback, 10)
        
        self.curr_x = 0.0
        self.curr_y = 0.0
        self.curr_yaw = 0.0
        self.get_logger().info('Follower Node가 데이터를 기다리는 중...')

    def odom_callback(self, msg):
        self.curr_x = msg.pose.pose.position.x
        self.curr_y = msg.pose.pose.position.y
        q = msg.pose.pose.orientation
        self.curr_yaw = math.atan2(2*(q.w*q.z + q.x*q.y), 1-2*(q.y*q.y + q.z*q.z))

    def target_callback(self, msg):
        # 데이터가 들어오면 터미널에 출력됩니다.
        self.get_logger().info(f'목표 수신! -> x:{msg.x:.2f}, y:{msg.y:.2f}')
        
        dx = msg.x - self.curr_x
        dy = msg.y - self.curr_y
        dist = math.sqrt(dx**2 + dy**2)
        angle_to_target = math.atan2(dy, dx)
        angle_error = math.atan2(math.sin(angle_to_target - self.curr_yaw), math.cos(angle_to_target - self.curr_yaw))

        twist = Twist()
        if dist > 0.1:
            twist.linear.x = min(0.5 * dist, 0.22)
            twist.angular.z = 1.5 * angle_error
        else:
            twist.linear.x = 0.0
            twist.angular.z = 0.0
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