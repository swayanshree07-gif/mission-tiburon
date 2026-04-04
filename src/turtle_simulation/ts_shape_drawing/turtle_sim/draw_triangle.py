#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import math
import time

class TurtleShape(Node):
    def __init__(self):
        super().__init__('turtle_shape')
        self.publisher = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.twist = Twist()
        time.sleep(2)  # Wait for turtlesim to start

    def move_forward(self, distance, speed=1.0):
        self.twist.linear.x = speed
        self.twist.angular.z = 0.0
        duration = distance / speed
        end_time = self.get_clock().now().nanoseconds / 1e9 + duration
        while self.get_clock().now().nanoseconds / 1e9 < end_time:
            self.publisher.publish(self.twist)
        self.twist.linear.x = 0.0
        self.publisher.publish(self.twist)

    def rotate(self, angle_deg, angular_speed=1.0):
        self.twist.linear.x = 0.0
        self.twist.angular.z = angular_speed if angle_deg > 0 else -angular_speed
        duration = math.radians(abs(angle_deg)) / angular_speed
        end_time = self.get_clock().now().nanoseconds / 1e9 + duration
        while self.get_clock().now().nanoseconds / 1e9 < end_time:
            self.publisher.publish(self.twist)
        self.twist.angular.z = 0.0
        self.publisher.publish(self.twist)

def main(args=None):
    rclpy.init(args=args)
    turtle = TurtleShape()
    
    for _ in range(3):  # Triangle has 3 sides
        turtle.move_forward(2.0, speed=1.5)
        turtle.rotate(120, angular_speed=1.0)

    turtle.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
