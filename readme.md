# Common Setup Guide (All Tasks)

This guide provides the **system requirements** and **initial setup steps** required to run all tasks in this repository.

## System Requirements

Ensure your system meets the following:

* **OS:** Ubuntu 22.04 / 24.04 (Linux recommended)
* **ROS2 Distribution:** Humble / Rolling (based on your setup) (Install ROS2 and its dependencies)
* **Python:** Python 3.10+

## Required Installations

### 1. Turtlesim

```bash
sudo apt install ros-humble-turtlesim
```

### 2. GUI Libraries (for Tkinter / PyQt)

Tkinter:

```bash
sudo apt install python3-tk
```

PyQt (optional alternative):

```bash
sudo apt install python3-pyqt5
```

### 4. OpenCV (for Perception Tasks)

```bash
pip install opencv-python
```

### 6. Additional Python Packages

```bash
pip install numpy
```

## Workspace Setup

```bash
mkdir -p ~/my_ws/src
cd ~/my_ws/src

git clone git@github.com:swayanshree07-gif/tiburon-inductions.git

cd ~/my_ws/src/tiburon-inductions
mv src/* .
rm -r src

cd ~/my_ws
colcon build
source install/setup.bash
```

## Ready to Go

You are now ready to run all tasks.

➡️ Refer to individual task folders for specific instructions.
