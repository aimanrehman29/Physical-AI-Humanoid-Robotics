---
id: physical-ai
title: Chapter 1 — Introduction to Physical AI
sidebar_position: 2
---

## Why this chapter

Physical AI blends software intelligence with bodies that sense and act in the physical world. This chapter sets the mental model for how data, models, and hardware come together safely.

### Learning goals

- Explain Physical AI in plain language and why embodiment matters.  
- Name core building blocks (sensing, perception, planning, control, actuation, safety).  
- Describe the sense → think → act loop and what to log for reliability.

## What is Physical AI?

AI that can perceive, decide, and act through a body. Key properties:

- **Grounded**: Uses real-world signals (vision, audio, force) to stay aligned with reality.  
- **Interactive**: Must respond safely to people and environments.  
- **Observable**: Needs telemetry (logs/metrics/traces) to debug and improve.

## The loop (sense → think → act)

1. **Sense**: Cameras, IMU, encoders, tactile sensors capture state.  
2. **Think**: Perception (detect/segment/locate), reasoning (goal/constraints), planning (motion path).  
3. **Act**: Controllers send joint/velocity/torque commands to actuators.  
4. **Observe**: Monitor health (latency, errors), safety (force/speed limits), and outcomes (success/fail).  
5. **Improve**: Use logs and feedback to adjust models, prompts, and limits.

## Safety anchors

- **E-stop**: Physical and software stop available and tested.  
- **Limits**: Speed/force caps near humans; compliant control preferred.  
- **Awareness**: Detect slips or unexpected contact via IMU/force; auto-abort and alert.  
- **Traceability**: Log decisions, inputs, and outputs for postmortem.

## Ready checklist for any demo

- [ ] E-stop reachable; stop/clear steps documented.  
- [ ] Speed/force limits set for the space.  
- [ ] Sensors healthy (camera/IMU/encoders OK).  
- [ ] Perception spot-check (target visible/detectable).  
- [ ] Logging on (rosbag or equivalent) with space available.
