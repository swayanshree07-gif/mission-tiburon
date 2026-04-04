#!/usr/bin/env python3

import rclpy
from rclpy.node import Node

from sensor_msgs.msg import Imu
from std_msgs.msg import String

from message_filters import Subscriber, ApproximateTimeSynchronizer


class SyncNode(Node):

    def __init__(self):
        super().__init__('sync_node')

        self.imu_sub = Subscriber(self, Imu, 'imu_data')
        self.cam_sub = Subscriber(self, String, 'camera_data')

        self.sync = ApproximateTimeSynchronizer(
            [self.imu_sub, self.cam_sub],
            queue_size=10,
            slop=0.1,
            allow_headerless=True   # ADD THIS
        )

        self.sync.registerCallback(self.callback)

    def callback(self, imu_msg, cam_msg):
        self.get_logger().info("------ SYNCED DATA ------")
        self.get_logger().info(f"IMU: {imu_msg.linear_acceleration.x}, {imu_msg.linear_acceleration.y}")
        self.get_logger().info(f"Camera: {cam_msg.data}")


def main(args=None):
    rclpy.init(args=args)
    node = SyncNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
