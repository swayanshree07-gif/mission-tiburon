# TURTLE SIMULATION : GUI Services

**Use Python Tkinter or PyQt to create buttons that call ROS2 services like reset, clear, or spawn turtles or change color of pen of turtle**

![Alt text](media/GUI_controls.png)

![TurtleSim GUI Demo](media/output.gif)

> Watch the full demo [here](https://drive.google.com/file/d/1lvBc8dLjjm3OiFL19Wc-HcDPhxq2roky/view?usp=drive_link)

```bash
cd ~/tiburon_ws
colcon build
```

## Terminal 1:
```bash
source install/setup.bash
ros2 run turtlesim turtlesim_node
```

## Terminal 2:
```bash
source install/setup.bash
ros2 run turtle_gui_pkg turtle_gui
```

