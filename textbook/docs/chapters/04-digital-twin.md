---
id: digital-twin
title: Chapter 4 — Digital Twin Simulation (Gazebo + Isaac)
sidebar_position: 5
---

A digital twin is a virtual copy of the robot and its environment. You test motions and perception in simulation before trying them on hardware.

## Why simulate first

- Catch collisions and balance issues safely.  
- Prototype perception and navigation without sensors wearing out.  
- Run faster-than-real-time for iteration.

## Gazebo quick start

```bash
sudo apt install ros-humble-gazebo-ros-pkgs   # example distro
ros2 launch gazebo_ros gazebo.launch.py
```

Spawn a model via ROS 2 service:

```bash
ros2 service call /spawn_entity gazebo_msgs/srv/SpawnEntity "{name: 'bot', xml: '$(< model.sdf )'}"
```

Minimal SDF snippet (model.sdf):

```xml
<model name="base_bot">
  <link name="base_link">
    <collision name="base_collision">
      <geometry><box><size>0.4 0.3 0.2</size></box></geometry>
    </collision>
    <visual name="base_visual">
      <geometry><box><size>0.4 0.3 0.2</size></box></geometry>
    </visual>
  </link>
</model>
```

## NVIDIA Isaac Sim (overview)

- Physics and rendering optimized for robotics; strong support for cameras/LiDAR simulation.  
- Omniverse-based; supports ROS 2 bridges.  
- Use for photo-real perception tests or multi-robot scenes.

Typical flow:

1. Import or build the URDF/USD model.  
2. Add sensors (RGB, depth, LiDAR) with realistic noise.  
3. Connect the ROS 2 bridge to publish simulated topics (`/camera`, `/scan`).  
4. Run scenarios (pick/place, navigation) and record bags.

## Testing motion plans in sim

```bash
ros2 launch moveit_demo bringup_sim.launch.py   # example launch with MoveIt + Gazebo
ros2 topic echo /motion_plan                    # inspect planned trajectories
```

Tips:

- Keep gravity, mass, and friction realistic; unstable values make controllers misbehave.  
- Add contact sensors on feet/hands to catch slips.  
- Record rosbags in sim; replay against your code to debug deterministically.

## Ready checklist

- [ ] You can explain what a digital twin is and why to use it.  
- [ ] You can launch Gazebo and spawn a simple model.  
- [ ] You know Isaac Sim’s role (photo-real sensors, ROS 2 bridge) and when to choose it.
