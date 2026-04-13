# TURTLE SIMULATION : Follow the Girl

**Spawn a turtle. Name a turtle girl. make it move. And make another turtle follow the first one.** 

![Follow the Girl Simulation](media/output.gif)

```bash
cd ~/my_ws
colcon build --symlink-install
source install/setup.bash
```

## Terminal 1:
```bash
ros2 run turtlesim turtlesim_node
```

## Terminal 2:
```bash
ros2 run turtle_follow follow_girl
```

Watch the **girl (pink) moving randomly** and the **follower (blue) following the girl**.

> To Watch the Demo Videos and Images: [Click Here](https://drive.google.com/drive/folders/1Jf9TPWPhs3FzPAMwE5lNOGVHmVa2BfRJ?usp=drive_link)

