#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Imu

class ImuPublisher(Node):

    def __init__(self):
        super().__init__('imu_publisher')

        self.publisher_ = self.create_publisher(Imu, 'imu_data', 10)

        self.timer = self.create_timer(0.05, self.publish_data)  # 20 Hz

    def publish_data(self):
        msg = Imu()

        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = "imu_frame"

        msg.linear_acceleration.x = 1.0
        msg.linear_acceleration.y = 0.5

        self.publisher_.publish(msg)

        self.get_logger().info(f"IMU Published at {msg.header.stamp.sec}.{msg.header.stamp.nanosec}")


def main(args=None):
    rclpy.init(args=args)
    node = ImuPublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
