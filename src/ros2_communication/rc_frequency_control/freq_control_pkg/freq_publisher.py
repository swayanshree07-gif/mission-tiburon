#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class FrequencyPublisher(Node):

    def __init__(self):
        super().__init__('frequency_publisher')

        # Create publisher
        self.publisher_ = self.create_publisher(String, 'chatter', 10)

        # Set frequency (10 Hz → 0.1 sec)
        timer_period = 0.1
        self.timer = self.create_timer(timer_period, self.publish_message)

        self.counter = 0

    def publish_message(self):
        msg = String()

        # Get current time
        current_time = self.get_clock().now().to_msg()

        msg.data = f"Hello {self.counter} | Time: {current_time.sec}.{current_time.nanosec}"

        self.publisher_.publish(msg)

        # Print to terminal
        self.get_logger().info(msg.data)

        self.counter += 1


def main(args=None):
    rclpy.init(args=args)

    node = FrequencyPublisher()
    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
