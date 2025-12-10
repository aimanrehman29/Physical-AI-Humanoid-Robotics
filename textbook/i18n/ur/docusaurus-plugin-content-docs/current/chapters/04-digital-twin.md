---
id: digital-twin
title: باب 4 — ڈیجیٹل ٹوئن سمیولیشن (Gazebo + Isaac)
sidebar_position: 5
---

ڈیجیٹل ٹوئن روبوٹ اور ماحول کی مجازی نقل ہے۔ اصل ہارڈویئر سے پہلے حرکات، ادراک، اور تعامل کو سمیولیشن میں جانچا جاتا ہے۔

## پہلے سمیولیشن کیوں؟
- تصادم اور توازن کے مسائل محفوظ طریقے سے پکڑیں۔  
- سینسر تھکن کے بغیر ادراک/نیویگیشن آزمائیں۔  
- تیز رفتار (فاسٹر دان ریئل ٹائم) تکرار۔

## Gazebo فوری آغاز
```bash
sudo apt install ros-humble-gazebo-ros-pkgs   # مثال ڈسٹری بیوشن
ros2 launch gazebo_ros gazebo.launch.py
```
سروس سے ماڈل سپان:
```bash
ros2 service call /spawn_entity gazebo_msgs/srv/SpawnEntity "{name: 'bot', xml: '$(< model.sdf )'}"
```
کم از کم SDF خاکہ:
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

## NVIDIA Isaac Sim (جائزہ)
- فزکس/رینڈرنگ میں مضبوط، کیمرا/لیڈار سمیولیشن کے لیے موزوں۔  
- Omniverse بنیاد؛ ROS 2 برج کی حمایت۔  
- فوٹو ریئل ادراک ٹیسٹ اور ملٹی روبوٹ سینز کے لیے مفید۔

عام مراحل: ماڈل درآمد/تیار کریں، سینسرز شامل کریں، ROS 2 برج جوڑیں، منظرنامے چلائیں اور ریکارڈ کریں۔

## حرکت کے منصوبے سمیولیشن میں جانچنا
```bash
ros2 launch moveit_demo bringup_sim.launch.py
ros2 topic echo /motion_plan
```

نکات:
- گریوٹی، ماس، فرکشن حقیقی رکھیں؛ غیر حقیقی قدریں کنٹرولرز کو غیر مستحکم کرتی ہیں۔  
- ہاتھ/پاؤں پر کانٹیکٹ سینسرز پھسلن پکڑنے میں مدد دیتے ہیں۔  
- سمیولیشن میں rosbags ریکارڈ کریں؛ ڈیبگ کے لیے ری پلے کریں۔

## تیار ہونے کی چیک لسٹ
- [ ] ڈیجیٹل ٹوئن کیا ہے اور کیوں ضروری ہے بیان کر سکتے ہیں۔  
- [ ] Gazebo لانچ کر کے سادہ ماڈل سپان کر سکتے ہیں۔  
- [ ] Isaac Sim کا کردار (فوٹو ریئل سینسرز، ROS 2 برج) اور کب منتخب کرنا ہے جانتے ہیں۔
