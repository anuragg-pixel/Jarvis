import itertools
import subprocess
import threading
import time
import webbrowser
from urllib.parse import quote_plus

import pyautogui

import config

pyautogui.PAUSE = 0
pyautogui.FAILSAFE = True


def run_osascript(script):
    return subprocess.run(["osascript", "-e", script], capture_output=True, text=True)


class SystemControl:
    def __init__(self):
        self.screen_w, self.screen_h = pyautogui.size()
        self.cursor = None
        self.pending = {}
        self.lock = threading.Lock()
        self.counter = itertools.count()
        self.alive = True
        self.worker = threading.Thread(target=self.loop, daemon=True)
        self.worker.start()

    def loop(self):
        while self.alive:
            with self.lock:
                jobs = list(self.pending.values())
                self.pending = {}
            for fn, args in jobs:
                fn(*args)
            time.sleep(0.03)

    def submit(self, key, fn, *args):
        with self.lock:
            self.pending[key] = (fn, args)

    def stop(self):
        self.alive = False

    def move_cursor(self, nx, ny):
        m = config.ACTIVE_MARGIN
        ax = min(max((nx - m) / (1 - 2 * m), 0.0), 1.0)
        ay = min(max((ny - m) / (1 - 2 * m), 0.0), 1.0)
        target = (ax * self.screen_w, ay * self.screen_h)
        if self.cursor is None:
            self.cursor = target
        else:
            a = config.SMOOTHING_ALPHA
            self.cursor = (
                a * target[0] + (1 - a) * self.cursor[0],
                a * target[1] + (1 - a) * self.cursor[1],
            )
        x = min(max(self.cursor[0], 5), self.screen_w - 5)
        y = min(max(self.cursor[1], 5), self.screen_h - 5)
        pyautogui.moveTo(x, y)

    def release_cursor(self):
        self.cursor = None

    def click(self):
        pyautogui.click()

    def press(self, key):
        pyautogui.press(key)

    def get_volume(self):
        result = run_osascript("output volume of (get volume settings)")
        try:
            return int(result.stdout.strip())
        except ValueError:
            return 50

    def set_volume(self, level):
        level = int(min(max(level, 0), 100))
        self.submit("volume", self.apply_volume, level)

    def apply_volume(self, level):
        run_osascript("set volume output volume " + str(level))

    def step_brightness(self, direction):
        code = config.BRIGHTNESS_KEYCODE_UP if direction > 0 else config.BRIGHTNESS_KEYCODE_DOWN
        self.submit(("brightness", next(self.counter)), self.apply_keycode, code)

    def apply_keycode(self, code):
        run_osascript('tell application "System Events" to key code ' + str(code))

    def open_url(self, url):
        webbrowser.open(url)

    def play_on_youtube(self, query):
        webbrowser.open(config.YOUTUBE_SEARCH_URL + quote_plus(query))

    def open_app(self, name):
        subprocess.run(["open", "-a", name], capture_output=True)