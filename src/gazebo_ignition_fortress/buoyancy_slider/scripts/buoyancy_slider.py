import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32
import tkinter as tk

class BuoyancySlider(Node):

    def __init__(self):
        super().__init__('buoyancy_slider')
        self.pub = self.create_publisher(Float32, '/buoyancy_force', 10)

        self.root = tk.Tk()
        self.root.title("Buoyancy Control")

        self.slider = tk.Scale(self.root, from_=0, to=2000,
                               orient=tk.HORIZONTAL,
                               label="Buoyancy Force",
                               command=self.update_value)
        self.slider.pack()

        self.root.after(100, self.loop)
        self.root.mainloop()

    def update_value(self, val):
        msg = Float32()
        msg.data = float(val)
        self.pub.publish(msg)
        self.get_logger().info(f'Buoyancy: {val}')

    def loop(self):
        rclpy.spin_once(self, timeout_sec=0)
        self.root.after(100, self.loop)


def main(args=None):
    rclpy.init(args=args)
    node = BuoyancySlider()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
