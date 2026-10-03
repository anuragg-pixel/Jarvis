import time

import cv2
import mediapipe as mp

import config
from controller import GestureController
from gestures import PoseStabilizer, classify_static, points
from system_control import SystemControl
from voice import VoiceAssistant


def draw_text(frame, text, row):
    cv2.putText(frame, text, (10, 24 + 24 * row), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)


def main():
    capture = cv2.VideoCapture(config.CAMERA_INDEX, cv2.CAP_AVFOUNDATION)
    capture.set(cv2.CAP_PROP_FRAME_WIDTH, config.FRAME_WIDTH)
    capture.set(cv2.CAP_PROP_FRAME_HEIGHT, config.FRAME_HEIGHT)

    hands = mp.solutions.hands.Hands(
        static_image_mode=False,
        max_num_hands=config.MAX_HANDS,
        model_complexity=config.MODEL_COMPLEXITY,
        min_detection_confidence=config.DETECTION_CONFIDENCE,
        min_tracking_confidence=config.TRACKING_CONFIDENCE,
    )
    drawer = mp.solutions.drawing_utils

    control = SystemControl()
    voice = VoiceAssistant(control)
    controller = GestureController(control, voice)
    stabilizer = PoseStabilizer()

    enabled = True
    fps = 0.0
    previous = time.monotonic()

    while True:
        ok, frame = capture.read()
        if not ok:
            break
        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(rgb)
        now = time.monotonic()

        pts = None
        if result.multi_hand_landmarks:
            hand = result.multi_hand_landmarks[0]
            pts = points(hand)
            drawer.draw_landmarks(frame, hand, mp.solutions.hands.HAND_CONNECTIONS)

        raw = classify_static(pts) if pts else "none"
        stable, entered = stabilizer.update(raw)

        if enabled:
            controller.update(pts, stable, entered, stabilizer.held_for(), now)

        dt = now - previous
        previous = now
        if dt > 0:
            fps = 0.9 * fps + 0.1 * (1.0 / dt)

        draw_text(frame, "pose: " + stable, 0)
        draw_text(frame, "action: " + controller.label, 1)
        draw_text(frame, "fps: " + str(int(fps)), 2)
        draw_text(frame, "control: " + ("on" if enabled else "paused"), 3)
        if voice.listening:
            draw_text(frame, "voice: listening", 4)
        elif voice.result:
            draw_text(frame, "voice: " + voice.result, 4)

        cv2.imshow("Project Jarvis", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break
        if key == ord("p"):
            enabled = not enabled
            controller.release()

    control.stop()
    hands.close()
    capture.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()