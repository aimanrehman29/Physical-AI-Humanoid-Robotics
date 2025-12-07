---
id: capstone
title: Chapter 6 — Capstone Project (AI-Robot Pipeline)
sidebar_position: 7
---

You will build a simple AI-robot pipeline that combines perception, ROS 2 messaging, simulation, and a basic action loop.

## Project goals

- Detect a target object in a scene.  
- Announce a plan (“I will pick the red mug from the table”).  
- Move a simulated arm/effector toward the target in Gazebo/Isaac.  
- Log what happened for review.

## Architecture (high level)

```text
Camera -> Perception (detection/caption) -> Intent (JSON schema) -> Planner (ROS 2 node) -> Action (MoveIt/command) -> Feedback (logs + speech)
```

## Steps

1) **Set up simulation**: Launch Gazebo/Isaac with a table and a simple object (box/mug).  
2) **Perception**: Capture an image and run a detector or caption model; output target name + pose estimate.  
3) **Intent**: Fill the JSON schema (`intent`, `target`, `location_hint`, `safety`).  
4) **ROS 2 nodes**:  
   - Perception publisher: publishes target pose on a topic (`/target_pose`).  
   - Planner/action node: subscribes to `/target_pose`, plans a reach to the target, and sends a trajectory.  
5) **Execution**: Use MoveIt or a simple joint trajectory publisher to move the simulated arm.  
6) **Feedback**: Log success/failure and speak the outcome.  
7) **Review**: Replay logs/bags to debug; adjust safety limits and perception thresholds.

## Minimal ROS 2 message for target pose (example)

```text
std_msgs/Header header
string label        # "mug"
geometry_msgs/Pose pose
float32 confidence  # 0.0-1.0
```

## Testing checklist

- [ ] Perception publishes a target pose when the object is visible.  
- [ ] Planner receives the pose and publishes a trajectory.  
- [ ] The simulated arm reaches the target without collisions.  
- [ ] Safety: stop/abort works; max force/speed respected.  
- [ ] Logs/rosbags recorded and replayed successfully.  

## Demo script (talk track)

1. Show the simulated scene and name the target.  
2. Run the pipeline; narrate perception → intent → plan → action.  
3. Trigger a stop to show safety handling.  
4. Replay the bag to highlight observability.
