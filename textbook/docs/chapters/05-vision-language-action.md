---
id: vision-language-action
title: Chapter 5 — Vision-Language-Action Systems
sidebar_position: 6
---

Vision-language-action (VLA) links what a robot sees and hears to what it does. Keep the loop simple: **see → understand → decide → act**.

## Perception to language

- Use an image or depth frame → run detection/segmentation → produce labels or bounding boxes.  
- Optional: caption the scene (“a red mug on the left of the sink”) to make it easy to reason about locations.

Example (Python pseudo, single image):

```python
from PIL import Image
import torch
from transformers import AutoProcessor, AutoModelForVision2Seq

processor = AutoProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = AutoModelForVision2Seq.from_pretrained("Salesforce/blip-image-captioning-base")

image = Image.open("frame.jpg")
inputs = processor(image, return_tensors="pt")
out = model.generate(**inputs, max_new_tokens=30)
caption = processor.decode(out[0], skip_special_tokens=True)
print("Scene:", caption)
```

## Language to action

- Map captions or user commands to a small set of skills: move, grasp, place, look, speak.  
- Keep a command schema (intent + target + constraints) to avoid ambiguity.

Example intent schema (JSON):

```json
{
  "intent": "pick",
  "target": "mug",
  "location_hint": "left of sink",
  "safety": {"max_force": 5, "speed": "slow"}
}
```

## Action execution

- Use motion planning (MoveIt) for reach/pick/place.  
- Validate target is visible and reachable before moving.  
- Re-plan if perception changes; keep a timeout and a safe stop.

## Safety and guardrails

- Confirm targets verbally/visually (“Pick the red mug? yes/no”).  
- Limit force/speed near people; abort on unexpected contact.  
- Log camera frames, commands, and actions for traceability.

## Ready checklist

- [ ] You can describe “see → understand → decide → act” with one example.  
- [ ] You have a simple command schema for actions.  
- [ ] You enforce confirmations and safety limits before executing motions.
