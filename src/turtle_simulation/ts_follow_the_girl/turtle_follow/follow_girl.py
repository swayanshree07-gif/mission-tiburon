import rclpy
from rclpy.node import Node
from turtlesim.srv import Spawn, SetPen
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import random
import math
import time

class FollowGirlDistance(Node):
    def __init__(self):
        super().__init__('follow_girl_distance')

        self.get_logger().info("Initializing turtles...")

        # Girl turtle (default) → pink
        self.set_pen('/turtle1/set_pen', 255, 0, 255, 2, False)

        # Spawn follower at (4,4) → blue
        self.spawn_follower()
        self.set_pen('/follower/set_pen', 0, 0, 255, 2, False)

        # Pose subscribers
        self.girl_pose = None
        self.follower_pose = None
        self.create_subscription(Pose, '/turtle1/pose', self.update_girl, 10)
        self.create_subscription(Pose, '/follower/pose', self.update_follower, 10)

        # Publishers
        self.pub_girl = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.pub_follower = self.create_publisher(Twist, '/follower/cmd_vel', 10)

        # Timers
        self.create_timer(0.1, self.move_girl)
        self.create_timer(0.05, self.move_follower)

        # Girl current direction
        self.girl_angle = random.uniform(-math.pi, math.pi)

    # ----------------- Services -----------------
    def spawn_follower(self):
        client = self.create_client(Spawn, '/spawn')
        while not client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Waiting for spawn service...')
        req = Spawn.Request()
        req.x = 4.0
        req.y = 4.0
        req.theta = 0.0
        req.name = 'follower'
        client.call_async(req)
        time.sleep(0.5)

    def set_pen(self, topic, r, g, b, width, off):
        client = self.create_client(SetPen, topic)
        while not client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info(f'Waiting for pen service {topic}...')
        req = SetPen.Request()
        req.r = r
        req.g = g
        req.b = b
        req.width = width
        req.off = off
        client.call_async(req)

    # ----------------- Pose callbacks -----------------
    def update_girl(self, msg):
        self.girl_pose = msg

    def update_follower(self, msg):
        self.follower_pose = msg

    # ----------------- Movement -----------------
    def move_girl(self):
        if self.girl_pose is None:
            return

        twist = Twist()
        margin = 0.5

        # Bounce back if hitting walls
        if self.girl_pose.x < margin:
            self.girl_angle = 0  # turn right
        elif self.girl_pose.x > 10.5 - margin:
            self.girl_angle = math.pi  # turn left
        elif self.girl_pose.y < margin:
            self.girl_angle = math.pi/2  # turn up
        elif self.girl_pose.y > 10.5 - margin:
            self.girl_angle = -math.pi/2  # turn down
        else:
            # small random variation
            self.girl_angle += random.uniform(-0.2, 0.2)

        # Move in current direction
        twist.linear.x = 1.0
        twist.angular.z = self.girl_angle - self.girl_pose.theta
        self.pub_girl.publish(twist)

    def move_follower(self):
        if self.follower_pose is None or self.girl_pose is None:
            return

        dx = self.girl_pose.x - self.follower_pose.x
        dy = self.girl_pose.y - self.follower_pose.y
        distance = math.sqrt(dx**2 + dy**2)
        angle_to_target = math.atan2(dy, dx)

        twist = Twist()

        # Maintain ~1 m distance
        if distance > 1:
            twist.linear.x = 1.0  # move
        else:
            twist.linear.x = 0.0  # stop

        twist.angular.z = angle_to_target - self.follower_pose.theta
        self.pub_follower.publish(twist)

def main(args=None):
    rclpy.init(args=args)
    node = FollowGirlDistance()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == "__main__":
    main()
