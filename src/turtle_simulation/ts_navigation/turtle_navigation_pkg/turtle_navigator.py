import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import math
import time

class TurtleNavigator(Node):
    def __init__(self):
        super().__init__('turtle_navigator')
        self.pose = None
        self.subscriber = self.create_subscription(Pose, '/turtle1/pose', self.pose_callback, 10)
        self.publisher = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.get_logger().info("Turtle Navigator Node Started!")

    def pose_callback(self, msg):
        self.pose = msg

    def move_to(self, target_x, target_y):
        while self.pose is None:
            rclpy.spin_once(self)

        while rclpy.ok():
            dx = target_x - self.pose.x
            dy = target_y - self.pose.y
            distance = math.sqrt(dx**2 + dy**2)

            if distance < 0.05:
                self.stop()
                print(f"Turtle has reached ({target_x}, {target_y})")
                break

            target_theta = math.atan2(dy, dx)
            angle_diff = target_theta - self.pose.theta
            if angle_diff > math.pi:
                angle_diff -= 2*math.pi
            elif angle_diff < -math.pi:
                angle_diff += 2*math.pi

            move_cmd = Twist()

            if abs(angle_diff) > 0.05:
                move_cmd.linear.x = 0.0
                move_cmd.angular.z = 2 * angle_diff
            else:
                move_cmd.linear.x = min(0.3, 0.5 * distance)
                move_cmd.angular.z = 0.0

            self.publisher.publish(move_cmd)
            rclpy.spin_once(self)
            time.sleep(0.05)

    def stop(self):
        move_cmd = Twist()
        move_cmd.linear.x = 0.0
        move_cmd.angular.z = 0.0
        self.publisher.publish(move_cmd)

def main(args=None):
    rclpy.init(args=args)
    navigator = TurtleNavigator()
    try:
        while True:
            print("\nEnter coordinates between 0 and 11")

            try:
                x = float(input("Enter target X (0-11): "))
                y = float(input("Enter target Y (0-11): "))

                # Input validation added here
                if not (0 <= x <= 11 and 0 <= y <= 11):
                    print("Invalid input! Please enter values between 0 and 11.\n")
                    continue

                navigator.move_to(x, y)

            except ValueError:
                print("Invalid input! Please enter numeric values.\n")
    except KeyboardInterrupt:
        navigator.stop()
    finally:
        navigator.destroy_node()
        rclpy.shutdown()

if __name__ == "__main__":
    main()
