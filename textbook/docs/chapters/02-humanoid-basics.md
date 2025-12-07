---
id: humanoid-basics
title: Chapter 2 — Basics of Humanoid Robotics
sidebar_position: 3
---

Humanoid robots mimic human form to operate tools and environments designed for people. This chapter keeps the concepts simple and visual.

## Core components (at a glance)

<details>
<summary>Head (sensing and compute)</summary>
Camera(s) for vision, microphone(s) for audio, embedded computer for perception and planning.
</details>

<details>
<summary>Torso (power and balance)</summary>
Houses batteries, main processor, IMU for balance, sometimes cooling and network modules.
</details>

<details>
<summary>Arms & hands (manipulation)</summary>
Actuators drive joints; end-effectors (hands/grippers) handle objects. Force/torque sensors protect against excessive force.
</details>

<details>
<summary>Legs & feet (locomotion)</summary>
Actuators, joint encoders, IMUs, and foot sensors keep balance and enable walking; sometimes wheels for hybrid mobility.
</details>

## Sensors (perception)

- **Vision**: RGB/depth cameras for object detection and pose estimation.  
- **Audio**: Microphones for speech commands and environment cues.  
- **Proprioception**: Joint encoders, IMU, force/torque at wrists/ankles for balance and safe contact.  
- **Tactile**: Pressure sensors in hands/skin for grasp feedback.

## Actuators (action)

- **Rotary/linear motors** for joints.  
- **Servos** for precise small motions (hands, head pan/tilt).  
- **Hydraulics** (heavier-duty robots) for high force.  
- **Compliance**: Series elastic or software torque limits to stay safe around people.

## Control loop (simple view)

```text
Sensors (vision, IMU, force) --> Perception (detect, estimate pose) --> Planning (where to move) --> Control (joint targets) --> Actuators
```

- Run this loop at two speeds: fast for balance, slower for perception and planning.

## Human-robot interaction basics

- **Voice + gestures**: Simple voice commands paired with arm/hand gestures.  
- **Feedback**: LEDs/tones/display to show status; small delays are explained (“thinking…”) to set expectations.  
- **Safety**: Keep clear stop actions; limit speed/force near humans; log interactions.

## Minimal anatomy sketch (inline SVG)

<svg width="240" height="320" viewBox="0 0 240 320" xmlns="http://www.w3.org/2000/svg">
  <g fill="none" stroke="#1f4bff" stroke-width="3" stroke-linecap="round">
    <rect x="80" y="40" width="80" height="90" rx="12" ry="12" fill="#e6edff"/>
    <circle cx="110" cy="80" r="8" fill="#1f4bff"/>
    <circle cx="150" cy="80" r="8" fill="#1f4bff"/>
    <path d="M120 130 L120 200" />
    <path d="M120 150 L80 200" />
    <path d="M120 150 L160 200" />
    <path d="M80 200 L100 260" />
    <path d="M160 200 L140 260" />
    <path d="M100 260 L90 300" />
    <path d="M140 260 L150 300" />
  </g>
</svg>

## Ready checklist

- [ ] You can name key parts (sensors, actuators, torso, limbs) and their roles.  
- [ ] You can describe a basic perception → planning → control loop.  
- [ ] You have clear stop/limit concepts for safe human interaction.
