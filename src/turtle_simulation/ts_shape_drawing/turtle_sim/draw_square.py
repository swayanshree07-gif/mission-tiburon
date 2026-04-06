#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from turtlesim.srv import SetPen, TeleportAbsolute
import time

class AnimatedSquare(Node):
    def __init__(self):
        super().__init__('animated_square')
        # Clients
        self.pen_client = self.create_client(SetPen, '/turtle1/set_pen')
        while not self.pen_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Waiting for /turtle1/set_pen service...')
        self.teleport_client = self.create_client(TeleportAbsolute, '/turtle1/teleport_absolute')
        while not self.teleport_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Waiting for /turtle1/teleport_absolute service...')

    # ---------------- Pen Control ---------------- #
    def pen_up(self):
        req = SetPen.Request()
        req.off = True
        req.width = 3
        req.r = req.g = req.b = 0
        self.pen_client.call_async(req)

    def pen_down(self, width=3, r=0, g=0, b=0):
        req = SetPen.Request()
        req.off = False
        req.width = width
        req.r = r
        req.g = g
        req.b = b
        self.pen_client.call_async(req)

    # ---------------- Smooth Move ---------------- #
    def move_to(self, x, y, steps=30):  # same speed as cube
        start_x, start_y = self.current_pos
        dx = (x - start_x) / steps
        dy = (y - start_y) / steps
        for i in range(1, steps+1):
            self.go_to(start_x + dx*i, start_y + dy*i)
            time.sleep(0.05)
        self.current_pos = (x, y)

    def go_to(self, x, y, theta=0.0):
        req = TeleportAbsolute.Request()
        req.x = float(x)
        req.y = float(y)
        req.theta = float(theta)
        self.teleport_client.call_async(req)
        time.sleep(0.01)

def main(args=None):
    rclpy.init(args=args)
    drawer = AnimatedSquare()

    # Square coordinates
    square_coords = [
        (5.0, 5.0),
        (2.0, 5.0),
        (2.0, 2.0),
        (5.0, 2.0),
        (5.0, 5.0)
    ]

    # Move to starting point without drawing
    drawer.current_pos = (5.0, 5.0)
    drawer.pen_up()
    drawer.move_to(*square_coords[0])
    drawer.pen_down()

    # Draw the square
    for coord in square_coords[1:]:
        drawer.move_to(*coord)

    drawer.pen_up()
    drawer.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
