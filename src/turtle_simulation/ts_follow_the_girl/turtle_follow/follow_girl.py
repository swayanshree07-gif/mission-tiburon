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

        # Spawn follower → blue
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

        # Initial direction
        self.girl_angle = random.uniform(-math.pi, math.pi)

    # ---------------- Services ----------------
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

    # ---------------- Pose callbacks ----------------
    def update_girl(self, msg):
        self.girl_pose = msg

    def update_follower(self, msg):
        self.follower_pose = msg

    # ---------------- Girl Movement ----------------
    def move_girl(self):
        if self.girl_pose is None:
            return

        twist = Twist()
        margin = 1.0

        x = self.girl_pose.x
        y = self.girl_pose.y
        theta = self.girl_angle

        # 🔮 Predict future position
        step = 0.8
        future_x = x + step * math.cos(theta)
        future_y = y + step * math.sin(theta)

        # 🚧 Avoid boundary BEFORE reaching it
        if (future_x < margin or future_x > 11 - margin or
            future_y < margin or future_y > 11 - margin):

            # Redirect toward center
            center_angle = math.atan2(5.5 - y, 5.5 - x)
            self.girl_angle = center_angle + random.uniform(-0.5, 0.5)

        else:
            # Smooth random wandering
            self.girl_angle += random.uniform(-0.2, 0.2)

        twist.linear.x = 1.0
        twist.angular.z = self.girl_angle - self.girl_pose.theta
        self.pub_girl.publish(twist)

    # ---------------- Follower Movement ----------------
    def move_follower(self):
        if self.follower_pose is None or self.girl_pose is None:
            return

        dx = self.girl_pose.x - self.follower_pose.x
        dy = self.girl_pose.y - self.follower_pose.y
        distance = math.sqrt(dx**2 + dy**2)

        angle_to_target = math.atan2(dy, dx)

        # 🔁 Normalize angle (VERY IMPORTANT)
        angle_error = angle_to_target - self.follower_pose.theta
        angle_error = math.atan2(math.sin(angle_error), math.cos(angle_error))

        twist = Twist()

        # 🎯 Rotate first if misaligned
        if abs(angle_error) > 0.5:
            twist.linear.x = 0.0
            twist.angular.z = 2.0 * angle_error

        else:
            # 🎯 Move only when aligned
            if distance > 1.0:
                twist.linear.x = 1.0
            else:
                twist.linear.x = 0.0

            twist.angular.z = 2.0 * angle_error

        self.pub_follower.publish(twist)


def main(args=None):
    rclpy.init(args=args)
    node = FollowGirlDistance()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()
