import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import time

class DrawSquare(Node):
    def __init__(self):
        super().__init__('draw_square')
        self.publisher_ = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)

    def move(self, linear_x, angular_z, duration):
        msg = Twist()
        msg.linear.x = linear_x
        msg.angular.z = angular_z

        start_time = time.time()
        while time.time() - start_time < duration:
            self.publisher_.publish(msg)

        # Stop after movement
        msg.linear.x = 0.0
        msg.angular.z = 0.0
        self.publisher_.publish(msg)

    def draw_square(self):
        for _ in range(4):
            # Move forward
            self.move(2.0, 0.0, 2)

            # Turn 90 degrees
            self.move(0.0, 1.57, 1)


def main(args=None):
    rclpy.init(args=args)
    node = DrawSquare()
    node.draw_square()
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
