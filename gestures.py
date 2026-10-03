import math
import time
from collections import deque

import config

WRIST = 0
THUMB_TIP = 4
INDEX_MCP = 5
INDEX_PIP = 6
INDEX_TIP = 8
MIDDLE_MCP = 9
MIDDLE_PIP = 10
MIDDLE_TIP = 12
RING_MCP = 13
RING_PIP = 14
RING_TIP = 16
PINKY_MCP = 17
PINKY_PIP = 18
PINKY_TIP = 20

FINGERS = (
    (INDEX_PIP, INDEX_TIP),
    (MIDDLE_PIP, MIDDLE_TIP),
    (RING_PIP, RING_TIP),
    (PINKY_PIP, PINKY_TIP),
)

PALM_POINTS = (WRIST, INDEX_MCP, MIDDLE_MCP, RING_MCP, PINKY_MCP)


def distance(a, b):
    return math.hypot(a[0] - b[0], a[1] - b[1])


def points(hand_landmarks):
    return [(p.x, p.y) for p in hand_landmarks.landmark]


def hand_scale(pts):
    return max(distance(pts[WRIST], pts[MIDDLE_MCP]), 1e-6)


def finger_states(pts):
    wrist = pts[WRIST]
    return [
        distance(pts[tip], wrist) > distance(pts[pip], wrist) * config.FINGER_MARGIN
        for pip, tip in FINGERS
    ]


def pinch_ratio(pts):
    return distance(pts[THUMB_TIP], pts[INDEX_TIP]) / hand_scale(pts)


def palm_center(pts):
    xs = sum(pts[i][0] for i in PALM_POINTS) / len(PALM_POINTS)
    ys = sum(pts[i][1] for i in PALM_POINTS) / len(PALM_POINTS)
    return xs, ys


def classify_static(pts):
    index, middle, ring, pinky = finger_states(pts)
    if middle and pinch_ratio(pts) < config.PINCH_RATIO:
        return "pinch"
    if index and not middle and not ring and not pinky:
        return "point"
    if index and middle and not ring and not pinky:
        return "two_fingers"
    if index and middle and ring and not pinky:
        return "three_fingers"
    if index and middle and ring and pinky:
        return "open_palm"
    if not (index or middle or ring or pinky):
        return "fist"
    return "none"


class PoseStabilizer:
    def __init__(self):
        self.candidate = "none"
        self.count = 0
        self.stable = "none"
        self.since = time.monotonic()

    def update(self, pose):
        if pose == self.candidate:
            self.count += 1
        else:
            self.candidate = pose
            self.count = 1
        entered = False
        if self.count >= config.PERSISTENCE_FRAMES and self.candidate != self.stable:
            self.stable = self.candidate
            self.since = time.monotonic()
            entered = True
        return self.stable, entered

    def held_for(self):
        return time.monotonic() - self.since


class SwipeDetector:
    def __init__(self):
        self.trail = deque()

    def reset(self):
        self.trail.clear()

    def update(self, center, now):
        self.trail.append((now, center[0], center[1]))
        while self.trail and now - self.trail[0][0] > config.SWIPE_WINDOW_SECONDS:
            self.trail.popleft()
        if len(self.trail) < 3:
            return None
        dx = self.trail[-1][1] - self.trail[0][1]
        dy = self.trail[-1][2] - self.trail[0][2]
        if abs(dx) >= config.SWIPE_MIN_DISTANCE and abs(dx) >= config.SWIPE_AXIS_RATIO * abs(dy):
            self.trail.clear()
            return "swipe_right" if dx > 0 else "swipe_left"
        return None