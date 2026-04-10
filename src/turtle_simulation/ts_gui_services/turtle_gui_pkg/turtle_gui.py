#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_srvs.srv import Empty
from turtlesim.srv import Spawn, SetPen
from geometry_msgs.msg import Twist
import tkinter as tk
from tkinter import ttk, messagebox
import threading
import math
import time

class TurtleController:
    """Controller for a single turtle"""
    def __init__(self, node: Node, name='turtle1'):
        self.node = node
        self.name = name
        self.cmd_vel_pub = self.node.create_publisher(Twist, f'/{name}/cmd_vel', 10)
        self.set_pen_client = self.node.create_client(SetPen, f'/{name}/set_pen')
        self.moving_forward = False
        self.moving_backward = False
        self.speed = 1.0

    def set_pen(self, r=255, g=0, b=0, width=3, off=0):
        while not self.set_pen_client.wait_for_service(timeout_sec=1.0):
            self.node.get_logger().info(f"Waiting for set_pen service for {self.name}...")
        req = SetPen.Request()
        req.r = r
        req.g = g
        req.b = b
        req.width = width
        req.off = off
        self.set_pen_client.call_async(req)

    def start_forward(self):
        self.moving_forward = True
        threading.Thread(target=self._move_continuous, args=(self.speed,), daemon=True).start()

    def start_backward(self):
        self.moving_backward = True
        threading.Thread(target=self._move_continuous, args=(-self.speed,), daemon=True).start()

    def stop(self):
        self.moving_forward = False
        self.moving_backward = False
        twist = Twist()
        twist.linear.x = 0.0
        twist.angular.z = 0.0
        self.cmd_vel_pub.publish(twist)

    def _move_continuous(self, speed):
        twist = Twist()
        twist.linear.x = speed
        while (self.moving_forward and speed > 0) or (self.moving_backward and speed < 0):
            self.cmd_vel_pub.publish(twist)
            time.sleep(0.05)
        twist.linear.x = 0.0
        twist.angular.z = 0.0
        self.cmd_vel_pub.publish(twist)

    def turn_right(self):
        twist = Twist()
        angular_speed = -1.5
        duration = math.pi/2 / abs(angular_speed)
        twist.angular.z = angular_speed
        start = time.time()
        while time.time() - start < duration:
            self.cmd_vel_pub.publish(twist)
            time.sleep(0.01)
        twist.angular.z = 0.0
        self.cmd_vel_pub.publish(twist)

    def turn_left(self):
        twist = Twist()
        angular_speed = 1.5
        duration = math.pi/2 / abs(angular_speed)
        twist.angular.z = angular_speed
        start = time.time()
        while time.time() - start < duration:
            self.cmd_vel_pub.publish(twist)
            time.sleep(0.01)
        twist.angular.z = 0.0
        self.cmd_vel_pub.publish(twist)


class TurtleSimGUI(Node):
    def __init__(self):
        super().__init__('turtle_gui_multi')
        self.reset_client = self.create_client(Empty, 'reset')
        self.clear_client = self.create_client(Empty, 'clear')
        self.spawn_client = self.create_client(Spawn, 'spawn')
        self.turtles = {}
        self.turtle_counter = 1  # next turtle number

        # Wait until /turtle1/cmd_vel exists
        ready = False
        while not ready:
            topics = self.get_topic_names_and_types()
            if any('/turtle1/cmd_vel' in t[0] for t in topics):
                ready = True
            else:
                self.get_logger().info("Waiting for /turtle1...")
                rclpy.spin_once(self, timeout_sec=0.5)

        # Default Turtle 1
        self.turtles[f"Turtle {self.turtle_counter}"] = TurtleController(self, name='turtle1')
        self.active_turtle = self.turtles[f"Turtle {self.turtle_counter}"]
        self.turtle_counter += 1

    def spawn_turtle(self, x, y):
        name = f"Turtle {self.turtle_counter}"
        self.turtle_counter += 1

        while not self.spawn_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info("Waiting for spawn service...")
        req = Spawn.Request()
        req.x = x
        req.y = y
        req.theta = 0.0
        req.name = name.replace(" ", "_").lower()
        self.spawn_client.call_async(req)

        turtle = TurtleController(self, name=req.name)
        self.turtles[name] = turtle
        self.active_turtle = turtle
        return name

    def reset(self):
        while not self.reset_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info("Waiting for reset service...")
        self.reset_client.call_async(Empty.Request())

    def clear(self):
        while not self.clear_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info("Waiting for clear service...")
        self.clear_client.call_async(Empty.Request())


# -------------------- Tkinter GUI --------------------
def start_gui(node: TurtleSimGUI):
    root = tk.Tk()
    root.title("TurtleSim Multi-Turtle Control")
    root.geometry("400x600")

    # --- Turtle selection ---
    tk.Label(root, text="Active Turtle").pack()
    turtle_var = tk.StringVar(value='Turtle 1')
    turtle_dropdown = ttk.Combobox(root, textvariable=turtle_var, state="readonly")
    turtle_dropdown['values'] = list(node.turtles.keys())
    turtle_dropdown.pack(pady=5)

    def change_active_turtle(event=None):
        if node.active_turtle:
            node.active_turtle.stop()
        selected = turtle_var.get()
        node.active_turtle = node.turtles[selected]

    turtle_dropdown.bind("<<ComboboxSelected>>", change_active_turtle)

    # --- Spawn button with coordinate input ---
    def spawn_new():
        coord_win = tk.Toplevel()
        coord_win.title("Spawn New Turtle")

        tk.Label(coord_win, text="X coordinate (0-11)").pack()
        x_entry = tk.Entry(coord_win)
        x_entry.pack()
        tk.Label(coord_win, text="Y coordinate (0-11)").pack()
        y_entry = tk.Entry(coord_win)
        y_entry.pack()

        def confirm_spawn():
            try:
                x = float(x_entry.get())
                y = float(y_entry.get())
            except ValueError:
                messagebox.showerror("Error", "Enter valid numbers for X and Y!")
                return
            # Strict boundary validation
            if not (0 <= x <= 11 and 0 <= y <= 11):
                messagebox.showerror(
                    "Invalid Coordinates",
                    "Coordinates must be between 0 and 11!"
                )
                return

            name = node.spawn_turtle(x, y)
            turtle_dropdown['values'] = list(node.turtles.keys())
            turtle_var.set(name)
            change_active_turtle()
            coord_win.destroy()

        tk.Button(coord_win, text="Spawn", command=confirm_spawn).pack(pady=5)

    tk.Button(root, text="Spawn Turtle", command=spawn_new).pack(pady=5)

    # --- Pen color ---
    tk.Label(root, text="Pen Color & Width").pack()
    tk.Label(root, text="R:").pack(); r_entry = tk.Entry(root); r_entry.pack()
    tk.Label(root, text="G:").pack(); g_entry = tk.Entry(root); g_entry.pack()
    tk.Label(root, text="B:").pack(); b_entry = tk.Entry(root); b_entry.pack()
    tk.Label(root, text="Width:").pack(); width_entry = tk.Entry(root); width_entry.pack()
    tk.Button(root, text="Change Pen", command=lambda: node.active_turtle.set_pen(
        r=int(r_entry.get()), g=int(g_entry.get()), b=int(b_entry.get()), width=int(width_entry.get())
    )).pack(pady=5)

    # --- Service buttons ---
    tk.Button(root, text="Reset", command=node.reset).pack(pady=5)
    tk.Button(root, text="Clear", command=node.clear).pack(pady=5)

    # --- Movement buttons ---
    tk.Label(root, text="Movement").pack(pady=5)

    movement_frame = tk.Frame(root)
    movement_frame.pack(pady=5)

    # Make grid responsive
    for i in range(3):
        movement_frame.grid_columnconfigure(i, weight=1)
        movement_frame.grid_rowconfigure(i, weight=1)

    # D-pad style layout
    tk.Button(movement_frame, text="Forward",
             command=lambda: node.active_turtle.start_forward(), width=10)\
       .grid(row=0, column=1, padx=3, pady=3)

    tk.Button(movement_frame, text="Left",
             command=lambda: node.active_turtle.turn_left(), width=10)\
       .grid(row=1, column=0, padx=3, pady=3)

    tk.Button(movement_frame, text="Stop",
             command=lambda: node.active_turtle.stop(), width=10)\
       .grid(row=1, column=1, padx=3, pady=3)

    tk.Button(movement_frame, text="Right",
             command=lambda: node.active_turtle.turn_right(), width=10)\
       .grid(row=1, column=2, padx=3, pady=3)

    tk.Button(movement_frame, text="Backward",
             command=lambda: node.active_turtle.start_backward(), width=10)\
       .grid(row=2, column=1, padx=3, pady=3)

    root.mainloop()


# -------------------- Main --------------------
def main():
    rclpy.init()
    node = TurtleSimGUI()
    threading.Thread(target=lambda: rclpy.spin(node), daemon=True).start()
    start_gui(node)


if __name__ == '__main__':
    main()
