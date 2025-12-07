---
id: ros2-fundamentals
title: Chapter 3 — ROS 2 Fundamentals
sidebar_position: 4
---

ROS 2 is a middleware that lets robot software pieces talk to each other. The three core concepts: **nodes** (processes), **topics** (pub/sub), and **services** (request/response).

## Core concepts

- **Node**: A process that does one focused job (camera driver, planner).  
- **Topic**: A named channel for streaming data (e.g., `/camera/color/image_raw`). Publishers send messages; subscribers receive them.  
- **Service**: A named endpoint for one-off calls (e.g., `/reset_pose`). Clients request; service servers respond.  
- **Parameters**: Runtime-tunable values (e.g., max speed).  
- **Launch files**: Start multiple nodes with configs.

## Minimal examples (Python, rclpy)

Publisher (talker):

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class Talker(Node):
    def __init__(self):
        super().__init__('talker')
        self.pub = self.create_publisher(String, 'chatter', 10)
        self.create_timer(0.5, self.tick)

    def tick(self):
        msg = String()
        msg.data = 'hello ROS 2'
        self.pub.publish(msg)
        self.get_logger().info(f'Pub: {msg.data}')

rclpy.init()
rclpy.spin(Talker())
rclpy.shutdown()
```

Subscriber (listener):

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class Listener(Node):
    def __init__(self):
        super().__init__('listener')
        self.create_subscription(String, 'chatter', self.cb, 10)

    def cb(self, msg: String):
        self.get_logger().info(f'Heard: {msg.data}')

rclpy.init()
rclpy.spin(Listener())
rclpy.shutdown()
```

Service (reset pose):

```python
from example_interfaces.srv import SetBool

class ResetPose(Node):
    def __init__(self):
        super().__init__('reset_pose_service')
        self.create_service(SetBool, 'reset_pose', self.handle)

    def handle(self, request, response):
        # reset logic here
        response.success = True
        response.message = 'Pose reset'
        return response
```

Launch (start talker + listener) — `demo.launch.py`:

```python
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(package='demo_pkg', executable='talker', name='talker'),
        Node(package='demo_pkg', executable='listener', name='listener'),
    ])
```

Run with:

```bash
ros2 launch demo_pkg demo.launch.py
```

## Graph and tools

- `ros2 node list`, `ros2 topic list`, `ros2 interface show <msg>` to inspect the graph.  
- `ros2 topic echo <topic>` to see messages.  
- `ros2 run tf2_tools view_frames` to visualize transforms.

## Ready checklist

- [ ] You can explain node/topic/service in one sentence each.  
- [ ] You can run a minimal publisher and subscriber.  
- [ ] You can launch multiple nodes and inspect topics with `ros2 topic list/echo`.
