# Jarvis

### Touch-free computer interaction through hand gestures and voice

Jarvis is a Python-based **multimodal Human-Computer Interaction (HCI) system** that allows users to control a computer through **hand gestures and voice commands**.

The system combines real-time hand tracking with offline speech recognition and translates recognized interactions into actions such as cursor movement, clicking, media control, volume and brightness adjustment, application launching, and YouTube control.

Jarvis is currently focused on exploring practical, low-cost, touch-free interaction using a webcam and microphone.

## Features

### Hand Gesture Control

Jarvis uses **MediaPipe Hands** and OpenCV to detect hand landmarks from a webcam feed and classify predefined gestures.

Supported interactions include:

| Gesture                       | Action               |
| ----------------------------- | -------------------- |
| Point                         | Move the cursor      |
| Pinch                         | Left click           |
| Open palm + horizontal swipe  | Navigate left/right  |
| Open palm + vertical movement | Adjust volume        |
| Two fingers                   | Adjust brightness    |
| Fist hold                     | Play / pause         |
| Three-finger hold             | Activate voice input |

Gesture detection includes temporal stabilization, cooldowns, hold detection, movement thresholds, and cursor smoothing to reduce accidental actions.

### Voice Control

Voice input is processed locally using **Vosk**, allowing Jarvis to recognize commands without relying on a cloud speech-recognition API.

Supported commands include:

* Open applications
* Open YouTube
* Search and play content on YouTube
* Increase/decrease volume
* Mute audio
* Increase/decrease brightness

The voice pipeline runs asynchronously so that speech processing does not block the main camera-processing loop.

### System Control

The system-control layer connects recognized gestures and voice commands to actual computer operations.

It currently supports:

* Cursor movement
* Mouse clicks
* Keyboard input
* Volume control
* Brightness control
* Application launching
* Web browser actions
* YouTube searches

The current implementation targets **macOS**, using PyAutoGUI and native macOS automation through AppleScript/`osascript`.

---

## Architecture

```text
                 ┌────────────────────┐
                 │       User         │
                 └─────────┬──────────┘
                           │
              ┌────────────┴────────────┐
              │                         │
              ▼                         ▼
       ┌──────────────┐         ┌────────────────┐
       │    Webcam    │         │   Microphone   │
       └──────┬───────┘         └───────┬────────┘
              │                         │
              ▼                         ▼
       ┌──────────────┐         ┌────────────────┐
       │   OpenCV +   │         │     Vosk       │
       │   MediaPipe  │         │ Speech Model   │
       └──────┬───────┘         └───────┬────────┘
              │                         │
              ▼                         ▼
       ┌──────────────┐         ┌────────────────┐
       │   Gesture    │         │     Voice      │
       │ Classification│         │Command Parsing │
       └──────┬───────┘         └───────┬────────┘
              │                         │
              └────────────┬────────────┘
                           ▼
                  ┌─────────────────┐
                  │    Controller   │
                  └────────┬────────┘
                           ▼
                  ┌─────────────────┐
                  │ System Control  │
                  └────────┬────────┘
                           ▼
                  ┌─────────────────┐
                  │     Computer    │
                  └─────────────────┘
```

## Project Structure

```text
Jarvis/
├── main.py              # Main application loop and camera processing
├── gestures.py          # Hand landmark processing and gesture classification
├── controller.py        # Maps gestures to system actions
├── system_control.py    # OS-level computer control
├── voice.py             # Offline voice recognition and command parsing
├── config.py             # Tunable thresholds, timings and mappings
├── requirements.txt      # Python dependencies
└── models/
    └── vosk-model-small-en-us-0.15/
                           # Local Vosk speech model
```

## Tech Stack

* **Python**
* **OpenCV** — Webcam capture and image processing
* **MediaPipe Hands** — Real-time hand landmark detection
* **Vosk** — Offline speech recognition
* **PyAutoGUI** — Mouse and keyboard automation
* **NumPy** — Numerical processing
* **AppleScript / `osascript`** — macOS system-level controls
* **SoundDevice** — Microphone input

The current dependency set is defined in `requirements.txt`.

## Getting Started

### Requirements

* macOS
* Python 3.9+
* Webcam
* Microphone

### Installation

```bash
git clone https://github.com/anuragg-pixel/Jarvis.git
cd Jarvis

python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
```

### Download the Vosk Model

The Vosk model is intentionally excluded from the repository because of its size.

Download:

```text
vosk-model-small-en-us-0.15
```

and place it at:

```text
models/vosk-model-small-en-us-0.15/
```

The path is configured in `config.py`.

### Run

```bash
python main.py
```

The application opens a webcam window showing the detected hand landmarks, current gesture, active action, FPS, control state, and voice status.

### Keyboard Controls

```text
Q  → Quit Jarvis
P  → Pause / resume gesture control
```

---

## Configuration

Most interaction parameters are centralized in `config.py`.

Examples include:

* Camera resolution
* Hand detection confidence
* Tracking confidence
* Gesture persistence
* Hold duration
* Gesture cooldowns
* Cursor smoothing
* Swipe distance
* Volume sensitivity
* Voice timeout
* Vosk model path
* Supported applications

This makes the interaction system easier to tune without changing the core implementation.

---

## Current Limitations

Jarvis is an experimental HCI prototype and currently has several limitations:

* System-level controls are implemented specifically for macOS.
* Gesture recognition uses rule-based geometric classification rather than a trained custom gesture-classification model.
* The supported vocabulary of voice commands is predefined.
* Recognition performance can be affected by lighting, hand visibility, camera position, background conditions, and speech clarity.
* The Vosk model must be downloaded separately.

These limitations also define several directions for future development.

---

## Roadmap

Future versions may explore:

* More robust gesture recognition
* Custom-trained gesture classification
* Better handling of multiple hands
* Expanded voice-command vocabulary
* Context-aware command interpretation
* Multimodal gesture + voice commands
* Application-specific controls
* Cross-platform system control
* AI-assisted intent recognition
* More advanced HCI experiments

---

## Project Status

**Phase 1 — Experimental HCI Prototype**

Jarvis is currently a working prototype for exploring touch-free computer interaction through computer vision and speech recognition.

The project is also intended as a foundation for future experiments involving intelligent and multimodal interfaces.

## License

License information will be added soon.
