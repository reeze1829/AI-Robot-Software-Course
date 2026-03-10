#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import TransformStamped, PointStamped
import tf2_ros
import tf2_geometry_msgs
import math

class FollowerDetectorNode(Node):
    def __init__(self):
        super().__init__('follower_detector_node')
        try:
            self.declare_parameter('use_sim_time', False)
        except rclpy.exceptions.ParameterAlreadyDeclaredException:
            pass
        
        self.tf_buffer = tf2_ros.Buffer()
        self.tf_listener = tf2_ros.TransformListener(self.tf_buffer, self)
        self.tf_broadcaster = tf2_ros.TransformBroadcaster(self)
        
        # 주 방식: 리더(TB3_1)가 뒤를 스캔
        self.subscription1 = self.create_subscription(
            LaserScan,
            '/TB3_1/scan',
            self.scan1_callback,
            rclpy.qos.qos_profile_sensor_data)
            
        # 보조 방식: 팔로워(TB3_2)가 앞을 스캔
        self.subscription2 = self.create_subscription(
            LaserScan,
            '/TB3_2/scan',
            self.scan2_callback,
            rclpy.qos.qos_profile_sensor_data)
            
        self.latest_odom_tf = None
        self.latest_scan_stamp = None
        
        self.last_tb3_1_detect_time = 0.0
        self.no_detect_count = 0           # 연속 감지 실패 카운터
        self.timer = self.create_timer(0.05, self.publish_tf)
        self.get_logger().info("Dual follower detector initialized. Waiting for scans...")

    def scan1_callback(self, msg):
        try:
            points = []
            for i, r in enumerate(msg.ranges):
                if r < msg.range_min or r > msg.range_max or math.isinf(r) or math.isnan(r):
                    continue
                ang = msg.angle_min + i * msg.angle_increment
                # TB3_1 등 뒤 직선 부채꼴 범위 (180도 ± 34도)
                if abs(ang) > 2.5:
                    if 0.15 < r < 1.5:
                        x = r * math.cos(ang)
                        y = r * math.sin(ang)
                        # 옆쪽 벽돌(벽면)을 오인식하지 않도록 좌우 폭(y)을 ±35cm로 제한
                        if abs(y) < 0.35:
                            points.append((x, y))
            
            if not points:
                self.no_detect_count += 1
                return

            self.no_detect_count = 0
            points.sort(key=lambda p: math.hypot(p[0], p[1]))
            closest = points[0]

            cluster = [p for p in points if math.hypot(p[0]-closest[0], p[1]-closest[1]) < 0.3]

            if len(cluster) < 3:
                return

            max_x = max(p[0] for p in cluster)
            min_x = min(p[0] for p in cluster)
            max_y = max(p[1] for p in cluster)
            min_y = min(p[1] for p in cluster)
            if (max_x - min_x) > 0.25 or (max_y - min_y) > 0.25:
                # 크기가 25cm를 초과하는 거대한 군집(벽이나 기둥 등)은 터틀봇(14cm)이 아니므로 무시
                return

            # 여기까지 오면 TB3_1 감지 성공
            self.last_tb3_1_detect_time = self.get_clock().now().nanoseconds / 1e9
            
            avg_x = sum(p[0] for p in cluster) / len(cluster)
            avg_y = sum(p[1] for p in cluster) / len(cluster)
            
            dist = math.hypot(avg_x, avg_y)
            center_dist = dist + 0.07  # 버거 로봇 반지름 보정 (~0.07m)
            angle = math.atan2(avg_y, avg_x)
            center_x = center_dist * math.cos(angle)
            center_y = center_dist * math.sin(angle)

            pt_in_scan = PointStamped()
            pt_in_scan.header = msg.header
            pt_in_scan.point.x = center_x
            pt_in_scan.point.y = center_y
            pt_in_scan.point.z = 0.0

            self.latest_scan_stamp = msg.header.stamp

            transform_scan_to_odom1 = self.tf_buffer.lookup_transform(
                'TB3_1/odom',
                'TB3_1/base_scan',
                rclpy.time.Time(),
                timeout=rclpy.duration.Duration(seconds=0.1))
            
            pt_in_odom1 = tf2_geometry_msgs.do_transform_point(pt_in_scan, transform_scan_to_odom1)

            transform_odom2_to_base2 = self.tf_buffer.lookup_transform(
                'TB3_2/odom',
                'TB3_2/base_footprint',
                rclpy.time.Time(),
                timeout=rclpy.duration.Duration(seconds=0.1))
            
            new_tf = TransformStamped()
            new_tf.header.frame_id = 'TB3_1/odom'
            new_tf.child_frame_id = 'TB3_2/odom'
            
            new_tf.transform.translation.x = pt_in_odom1.point.x - transform_odom2_to_base2.transform.translation.x
            new_tf.transform.translation.y = pt_in_odom1.point.y - transform_odom2_to_base2.transform.translation.y
            new_tf.transform.translation.z = pt_in_odom1.point.z - transform_odom2_to_base2.transform.translation.z
            new_tf.transform.rotation.w = 1.0
            
            if self.latest_odom_tf is None:
                self.latest_odom_tf = new_tf
                self.get_logger().info(f"[Leader] Initial follower detection at distance {dist:.2f}m")
            else:
                alpha = 0.25
                self.latest_odom_tf.transform.translation.x = (
                    (1 - alpha) * self.latest_odom_tf.transform.translation.x
                    + alpha * new_tf.transform.translation.x
                )
                self.latest_odom_tf.transform.translation.y = (
                    (1 - alpha) * self.latest_odom_tf.transform.translation.y
                    + alpha * new_tf.transform.translation.y
                )
                self.latest_odom_tf.transform.translation.z = (
                    (1 - alpha) * self.latest_odom_tf.transform.translation.z
                    + alpha * new_tf.transform.translation.z
                )

        except tf2_ros.LookupException as e:
            pass
        except tf2_ros.ExtrapolationException as e:
            pass
        except Exception as e:
            pass

    def scan2_callback(self, msg):
        current_time = self.get_clock().now().nanoseconds / 1e9
        # 주 방식(TB3_1 스캔) 0.5초 이내에 성공했다면, 보조 로직 스킵
        if (current_time - self.last_tb3_1_detect_time) < 0.5:
            return

        try:
            points = []
            for i, r in enumerate(msg.ranges):
                if r < msg.range_min or r > msg.range_max or math.isinf(r) or math.isnan(r):
                    continue
                ang = msg.angle_min + i * msg.angle_increment
                # TB3_2 정면 직선 부채꼴 범위 (0도 ± 34도)
                if abs(ang) < 0.6:
                    if 0.15 < r < 1.5:
                        x = r * math.cos(ang)
                        y = r * math.sin(ang)
                        # 옆쪽 벽돌(벽면)을 오인식하지 않도록 좌우 폭(y)을 ±35cm로 제한
                        if abs(y) < 0.35:
                            points.append((x, y))
            
            if not points:
                return

            points.sort(key=lambda p: math.hypot(p[0], p[1]))
            closest = points[0]

            cluster = [p for p in points if math.hypot(p[0]-closest[0], p[1]-closest[1]) < 0.3]

            if len(cluster) < 3:
                return
            
            max_x = max(p[0] for p in cluster)
            min_x = min(p[0] for p in cluster)
            max_y = max(p[1] for p in cluster)
            min_y = min(p[1] for p in cluster)
            if (max_x - min_x) > 0.25 or (max_y - min_y) > 0.25:
                # 크기가 25cm를 초과하는 거대한 군집(벽이나 기둥 등)은 터틀봇(14cm)이 아니므로 무시
                return
            
            avg_x = sum(p[0] for p in cluster) / len(cluster)
            avg_y = sum(p[1] for p in cluster) / len(cluster)
            
            dist = math.hypot(avg_x, avg_y)
            center_dist = dist + 0.07  # 버거 로봇 반지름 보정 (~0.07m)
            angle = math.atan2(avg_y, avg_x)
            center_x = center_dist * math.cos(angle)
            center_y = center_dist * math.sin(angle)

            pt_in_scan = PointStamped()
            pt_in_scan.header = msg.header
            pt_in_scan.point.x = center_x
            pt_in_scan.point.y = center_y
            pt_in_scan.point.z = 0.0

            self.latest_scan_stamp = msg.header.stamp

            # TB3_2의 scan 상 포인트를 TB3_2/odom 으로 변환
            transform_scan2_to_odom2 = self.tf_buffer.lookup_transform(
                'TB3_2/odom',
                'TB3_2/base_scan',
                rclpy.time.Time(),
                timeout=rclpy.duration.Duration(seconds=0.1))
            
            pt_in_odom2 = tf2_geometry_msgs.do_transform_point(pt_in_scan, transform_scan2_to_odom2)

            # TB3_1 의 기준 위치를 알아냄
            transform_odom1_to_base1 = self.tf_buffer.lookup_transform(
                'TB3_1/odom',
                'TB3_1/base_footprint',
                rclpy.time.Time(),
                timeout=rclpy.duration.Duration(seconds=0.1))
            
            # 수학적 모델:
            # pt_in_odom2 (TB3_2/odom 기준 TB3_1 위치) == ODOM2 -> TB3_1
            # transform_odom1_to_base1.translation (TB3_1/odom 기준 TB3_1 위치) == ODOM1 -> TB3_1
            # ODOM1 -> ODOM2 = (ODOM1 -> TB3_1) - (ODOM2 -> TB3_1)
            
            new_tf = TransformStamped()
            new_tf.header.frame_id = 'TB3_1/odom'
            new_tf.child_frame_id = 'TB3_2/odom'
            
            new_tf.transform.translation.x = transform_odom1_to_base1.transform.translation.x - pt_in_odom2.point.x
            new_tf.transform.translation.y = transform_odom1_to_base1.transform.translation.y - pt_in_odom2.point.y
            new_tf.transform.translation.z = transform_odom1_to_base1.transform.translation.z - pt_in_odom2.point.z
            new_tf.transform.rotation.w = 1.0
            
            if self.latest_odom_tf is None:
                self.latest_odom_tf = new_tf
                self.get_logger().info(f"[Follower] Initial leader detection at distance {dist:.2f}m")
            else:
                alpha = 0.25
                self.latest_odom_tf.transform.translation.x = (
                    (1 - alpha) * self.latest_odom_tf.transform.translation.x
                    + alpha * new_tf.transform.translation.x
                )
                self.latest_odom_tf.transform.translation.y = (
                    (1 - alpha) * self.latest_odom_tf.transform.translation.y
                    + alpha * new_tf.transform.translation.y
                )
                self.latest_odom_tf.transform.translation.z = (
                    (1 - alpha) * self.latest_odom_tf.transform.translation.z
                    + alpha * new_tf.transform.translation.z
                )

        except tf2_ros.LookupException as e:
            pass
        except tf2_ros.ExtrapolationException as e:
            pass
        except Exception as e:
            pass

    def publish_tf(self):
        now = self.get_clock().now().to_msg()
        if self.latest_odom_tf is not None:
            # Nav2 컨트롤러가 'Transform data too old' 에러를 뱉지 않도록 현재 시간(now)으로 스탬프 갱신
            self.latest_odom_tf.header.stamp = now
            self.tf_broadcaster.sendTransform(self.latest_odom_tf)
        else:
            # 초기 감지 전 fallback: TB3_1 뒤쪽 0.4m
            new_tf = TransformStamped()
            new_tf.header.frame_id = 'TB3_1/odom'
            new_tf.header.stamp = now
            new_tf.child_frame_id = 'TB3_2/odom'
            new_tf.transform.translation.x = -0.4
            new_tf.transform.rotation.w = 1.0
            self.tf_broadcaster.sendTransform(new_tf)

def main(args=None):
    rclpy.init(args=args)
    node = FollowerDetectorNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
