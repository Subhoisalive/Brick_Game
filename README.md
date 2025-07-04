# Brick_Game
# 🧱 Brick Out - Gesture Powered Arcade Game

An innovative and interactive **brick-breaking arcade game** controlled by **hand gestures** using your webcam! Break bricks, collect power-ups, and challenge your reflexes across **50 exciting levels**.


## 🎮 Features

- 👋 **Gesture Control:** Move the paddle using just your finger (via webcam & MediaPipe).
- 🧱 **Dynamic Levels:** Up to 50 increasingly difficult brick-breaking levels.
- 💥 **Power-Ups:** Collect `Life`, `Widen`, and `Multi-ball` boosts.
- 🏆 **High Scoreboard:** Displays top 3 high scores.
- 🔁 **Retry Menu:** Choose to:
  - Press `Y` to restart from **Level 1**
  - Press `H` to **replay the current level**
  - Press `N` to **quit the game**
- 🎨 Colorful and modern UI built with `pygame`.

---

## 📸 Preview

> Add gameplay screenshots or GIFs here.

---

## 🛠️ Technologies Used

- 🐍 Python 3.8+
- 🎮 Pygame
- 📷 OpenCV
- ✋ MediaPipe (Hand tracking)

---

## 🚀 Getting Started

### 📦 Install Dependencies

```bash
pip install pygame opencv-python mediapipe
````

### ▶️ Run the Game

```bash
python brickout.py
```

> A webcam window will appear. Move your index finger left/right to control the paddle.

---

## 🎯 Controls

| Action             | Key                         |
| ------------------ | --------------------------- |
| Move Paddle        | 👆 Your Finger (via webcam) |
| Retry from Level 1 | `Y`                         |
| Replay same level  | `H`                         |
| Quit game          | `N`                         |
| Quit webcam        | `Q` in the webcam window    |

---

## 📁 File Structure

```
brickout/
├── brickout.py        # Main game script
├── scores.txt         # High scores saved here
├── README.md          # Game documentation
```

---

## 🙌 Credits

* Created by [Suvhankar Dutta](https://github.com/Subhoisalive)
* Hand Tracking powered by [MediaPipe](https://mediapipe.dev/)
* Built using [Pygame](https://www.pygame.org/)

---

## 📜 License

This project is licensed under the [MIT License](LICENSE).

