# Jarvis

A touch-free computer control system built around **voice and hand gestures**, using Python, OpenCV, MediaPipe, and Vosk.

Jarvis combines real-time gesture recognition with voice commands to interact with and control the computer without traditional input devices.

This is **Phase 1** of a longer-term exploration into Human-Computer Interaction (HCI), intelligent interfaces, and multimodal computer control.

## Features

* **Gesture Recognition** — Real-time hand tracking and gesture classification using MediaPipe and OpenCV
* **Voice Commands** — Offline speech recognition using Vosk
* **System Control** — Converts recognized gestures and voice commands into OS-level actions such as volume, media, and cursor controls
* **Configurable Controls** — Gesture and voice mappings are centralized in `config.py` for easy customization
* **Touch-Free Interaction** — Designed to experiment with natural, multimodal interaction between humans and computers

## Project Structure

```text
Jarvis/
├── main.py              # Entry point
├── gestures.py          # Hand gesture detection and classification
├── controller.py        # Maps gestures/commands to system actions
├── system_control.py    # OS-level controls
├── voice.py             # Voice command recognition and processing
├── config.py            # Configuration and mappings
├── models/              # Local speech recognition model
└── requirements.txt     # Python dependencies
```

> **Note:** The Vosk model is not included in this repository because of its size. Download the required model separately and place it inside the `models/` directory.

## Tech Stack

* **Python**
* **OpenCV** — Computer vision and webcam processing
* **MediaPipe** — Hand tracking and gesture recognition
* **Vosk** — Offline speech recognition

## Getting Started

### Prerequisites

* Python 3.9+
* Webcam
* Microphone
* macOS/Linux/Windows environment with the required system-control dependencies

### Installation

Clone the repository:

```bash
git clone https://github.com/anuragg-pixel/Jarvis.git
cd Jarvis
```

Create and activate a virtual environment:

**macOS / Linux**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows**

```bash
python -m venv .venv
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

### Vosk Model

Download the required Vosk speech recognition model and place it at:

```text
models/vosk-model-small-en-us-0.15/
```

The model directory is intentionally excluded from Git.

### Usage

Run Jarvis with:

```bash
python main.py
```

## Roadmap

Jarvis is currently **Phase 1** of a broader HCI-focused project roadmap.

Future development may explore:

* Improved gesture recognition
* More natural voice interaction
* Multimodal intent recognition
* Context-aware commands
* Deeper system and application integration
* AI-assisted interaction
* Expansion toward a broader HCI assistant ecosystem

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
