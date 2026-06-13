# Aline

<div align="center">

```
  __   __    __  __ _  ____ 
 / _\ (  )  (  )(  ( \(  __)
/    \/ (_/\ )( /    / ) _) 
\_/\_/\____/(__)\_)__)(____)
```

### A tiny desktop companion that walks, idles, jumps, and lives on your desktop.

</div>

---

## About

**Aline** is a lightweight desktop companion built with **Python** and **PySide6**.

The character is based on a pixel-art version of my girlfriend and was created as an experiment in desktop overlays, sprite animation, and autonomous behavior.

Aline lives above every other window, wandering along the bottom of your screen on her own. She can walk, idle, jump, and react when picked up and moved around, giving the impression of a small animated character quietly inhabiting your desktop.

Her behavior is driven by a sprite-based animation system and a simple state machine, allowing her to feel alive while remaining lightweight and unobtrusive.

---

## Preview

<div align="center">

![Aline](./aline.png)

</div>

---

## Demo Video

A short recording of Aline in action:

* [Demo video](./videos_demo/demonstration.mp4)

---

## Features

* Frameless transparent overlay
* Always-on-top desktop companion
* Smooth sprite-based animations
* Idle, walk and jump states
* Autonomous movement across the screen
* Bidirectional walking with mirrored sprites
* Draggable with mouse interaction
* Randomized state durations for more natural behavior
* Window mask follows the visible sprite shape
* Lightweight and responsive

---

## Tech Stack

* **Language:** Python 3
* **GUI Framework:** PySide6 (Qt 6)
* **Rendering:** QPixmap + QPainter
* **Animation Loop:** QTimer (~60 FPS)

---

## Running

```bash
pip install pyside6
python main.py
```

---

## Project Structure

```text
.
├── main.py                 # Main window and behavior logic
├── animation.py            # Sprite animation system
├── robot.png               # Character preview image
├── assets/
│   ├── idle/
│   ├── walk/
│   ├── jump/
│   └── sleep/
└── videos_demo/
    └── demonstration.mp4
```

---

## Roadmap

Planned improvements include:

* Additional animation states
* Speech bubbles
* Mouse-following behavior
* Multiple companion personalities
* Sound effects
* Improved movement and pathfinding
* Integration with the future Athena project

---

## Why This Project Exists

Aline began as a personal project to explore desktop overlays, animation systems, and autonomous characters using Python and Qt.

What started as a technical experiment gradually became a small digital companion inspired by someone important to me.

The goal is not to create a game or a virtual pet, but a lightweight character that quietly shares space on the desktop and feels alive through simple animations and behaviors.

---

## License

**All rights reserved.**

This repository contains private proprietary software.

No permission is granted to use, copy, modify, distribute, sublicense, publish, or create derivative works from this software without explicit prior written permission from the author.

Unauthorized use of any portion of this project is prohibited.

© Author. All rights reserved.
