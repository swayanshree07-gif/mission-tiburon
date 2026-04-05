#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from turtlesim.srv import SetPen, TeleportAbsolute
import time

class CubeDrawer(Node):
    def __init__(self):
        super().__init__('cube_drawer')
        # Clients for pen control and teleport
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

    # ---------------- Move to coordinate ---------------- #
    def go_to(self, x, y, theta=0.0):
        req = TeleportAbsolute.Request()
        req.x = float(x)  # Ensure float type
        req.y = float(y)
        req.theta = float(theta)
        self.teleport_client.call_async(req)
        time.sleep(0.1)  # small pause to ensure teleport completes

# ---------------- Main ---------------- #
def main(args=None):
    rclpy.init(args=args)
    drawer = CubeDrawer()

    # Define cube coordinates (all floats)
    front_bottom_left  = (5.54445, 5.54445)
    front_bottom_right = (7.54445, 5.54445)
    front_top_right    = (7.54445, 7.54445)
    front_top_left     = (5.54445, 7.54445)

    back_bottom_left   = (6.54445, 6.54445)
    back_bottom_right  = (8.54445, 6.54445)
    back_top_right     = (8.54445, 8.54445)
    back_top_left      = (6.54445, 8.54445)

    edges = [
        # Front face
        (front_bottom_left, front_bottom_right),
        (front_bottom_right, front_top_right),
        (front_top_right, front_top_left),
        (front_top_left, front_bottom_left),

        # Back face
        (back_bottom_left, back_bottom_right),
        (back_bottom_right, back_top_right),
        (back_top_right, back_top_left),
        (back_top_left, back_bottom_left),

        # Connect front to back
        (front_bottom_left, back_bottom_left),
        (front_bottom_right, back_bottom_right),
        (front_top_right, back_top_right),
        (front_top_left, back_top_left)
    ]

    # Draw all edges
    for start, end in edges:
        drawer.pen_up()
        drawer.go_to(*start)
        drawer.pen_down()
        drawer.go_to(*end)

    drawer.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
