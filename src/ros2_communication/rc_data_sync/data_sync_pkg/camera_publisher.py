#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from std_msgs.msg import Header
from std_msgs.msg import String
from rclpy.time import Time

class CameraPublisher(Node):

    def __init__(self):
        super().__init__('camera_publisher')

        self.publisher_ = self.create_publisher(String, 'camera_data', 10)

        self.timer = self.create_timer(0.1, self.publish_data)  # 10 Hz

    def publish_data(self):
        msg = String()

        current_time = self.get_clock().now().to_msg()
        # create a header timestamp
        now = self.get_clock().now().to_msg()

        msg.data = f"Object detected at {current_time.sec}.{current_time.nanosec}"

        self.publisher_.publish(msg)

        self.get_logger().info(msg.data)


def main(args=None):
    rclpy.init(args=args)
    node = CameraPublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
