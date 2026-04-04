#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import time
import math
from turtlesim.srv import SetPen

class TurtleCube(Node):
    def __init__(self):
        super().__init__('turtle_cube')
        self.pub = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.twist = Twist()
        time.sleep(2)  # wait for turtlesim to fully start

    # ------------------ Movement Functions ------------------ #
    def move(self, distance, speed=0.5):
        """Move turtle forward by distance (m) at given speed."""
        self.twist.linear.x = speed
        self.twist.angular.z = 0.0
        start_time = self.get_clock().now().nanoseconds / 1e9
        duration = distance / speed
        while self.get_clock().now().nanoseconds / 1e9 - start_time < duration:
            self.pub.publish(self.twist)
            time.sleep(0.02)  # small sleep for smooth movement
        self.twist.linear.x = 0.0
        self.pub.publish(self.twist)

    def rotate(self, angle_deg, angular_speed_deg=30.0):
        """Rotate turtle by angle in degrees. Positive=left, Negative=right."""
        angular_speed = math.radians(angular_speed_deg)
        direction = 1 if angle_deg > 0 else -1
        self.twist.linear.x = 0.0
        self.twist.angular.z = direction * angular_speed
        start_time = self.get_clock().now().nanoseconds / 1e9
        duration = abs(math.radians(angle_deg) / angular_speed)
        while self.get_clock().now().nanoseconds / 1e9 - start_time < duration:
            self.pub.publish(self.twist)
            time.sleep(0.02)
        self.twist.angular.z = 0.0
        self.pub.publish(self.twist)

    # ------------------ Pen Control Functions ------------------ #
    def pen_up(self):
        client = self.create_client(SetPen, '/turtle1/set_pen')
        while not client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Waiting for /turtle1/set_pen service...')
        req = SetPen.Request()
        req.off = True
        future = client.call_async(req)
        rclpy.spin_until_future_complete(self, future)

    def pen_down(self, width=3, r=0, g=0, b=0):
        """Put pen down with fixed width & color to maintain consistent lines."""
        client = self.create_client(SetPen, '/turtle1/set_pen')
        while not client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Waiting for /turtle1/set_pen service...')
        req = SetPen.Request()
        req.off = False
        req.width = width
        req.r = r
        req.g = g
        req.b = b
        future = client.call_async(req)
        rclpy.spin_until_future_complete(self, future)

# ------------------ Main ------------------ #
def main(args=None):
    rclpy.init(args=args)
    turtle = TurtleCube()

    # ------------------ Draw first square ------------------ #
    turtle.pen_down(width=3)
    for _ in range(4):
        turtle.move(2.0)
        turtle.rotate(90)

    # ------------------ Offset for second square ------------------ #
    turtle.rotate(45)
    turtle.move(0.5)
    turtle.rotate(-45)

    # ------------------ Draw second square ------------------ #
    for _ in range(4):
        turtle.move(2.0)
        turtle.rotate(90)

    # ------------------ Cube connections with pen control ------------------ #
    # Step 1
    turtle.pen_up()
    time.sleep(0.1)
    turtle.move(2.0)
    turtle.rotate(-135)
    turtle.pen_down(width=3)
    turtle.move(0.5)
    turtle.rotate(-135)

    # Step 2
    turtle.pen_up()
    time.sleep(0.1)
    turtle.move(2.0)
    turtle.rotate(-45)
    turtle.pen_down(width=3)
    turtle.move(0.5)

    # Step 3
    turtle.rotate(135)
    turtle.pen_up()
    time.sleep(0.1)
    turtle.move(2.0)
    turtle.rotate(45)
    turtle.pen_down(width=3)
    turtle.move(0.5)

    # Restore
    turtle.rotate(45)
    turtle.pen_up()
    turtle.move(2.0)
    turtle.rotate(90)
    turtle.pen_down()

    # ------------------ Finish ------------------ #
    turtle.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
