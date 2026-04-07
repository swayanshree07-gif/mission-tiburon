# TURTLE SIMULATION : Follow the Girl

**Spawn a turtle. Name a turtle girl. make it move. And make another turtle follow the first one.** 

![Follow the Girl Simulation](media/output.gif)

```bash
cd ~/tiburon_ws
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

