import config
from gestures import INDEX_TIP, SwipeDetector, palm_center


class GestureController:
    def __init__(self, control, voice):
        self.control = control
        self.voice = voice
        self.swipe = SwipeDetector()
        self.volume_anchor = None
        self.volume_base = 0
        self.brightness_anchor = None
        self.cooldowns = {}
        self.hold_fired = False
        self.label = "idle"

    def ready(self, name, seconds, now):
        if now - self.cooldowns.get(name, 0.0) >= seconds:
            self.cooldowns[name] = now
            return True
        return False

    def release(self):
        self.control.release_cursor()
        self.swipe.reset()
        self.volume_anchor = None
        self.brightness_anchor = None
        self.hold_fired = False

    def update(self, pts, stable, entered, held, now):
        if pts is None or stable == "none":
            self.release()
            self.label = "idle"
            return self.label
        if entered:
            self.release()
        center = palm_center(pts)
        if stable == "point":
            tip = pts[INDEX_TIP]
            self.control.move_cursor(tip[0], tip[1])
            self.label = "cursor"
        elif stable == "pinch":
            if entered and self.ready("click", config.CLICK_COOLDOWN_SECONDS, now):
                self.control.click()
                self.label = "click"
        elif stable == "open_palm":
            direction = self.swipe.update(center, now)
            if direction and self.ready("swipe", config.COOLDOWN_SECONDS, now):
                self.control.press("right" if direction == "swipe_right" else "left")
                self.label = direction
            else:
                self.adjust_volume(center[1])
        elif stable == "two_fingers":
            self.adjust_brightness(center[1])
        elif stable in ("fist", "three_fingers"):
            if (
                not self.hold_fired
                and held >= config.HOLD_SECONDS
                and self.ready(stable, config.COOLDOWN_SECONDS, now)
            ):
                self.hold_fired = True
                if stable == "fist":
                    self.control.press("space")
                    self.label = "play_pause"
                else:
                    self.voice.start_listening()
                    self.label = "voice"
        return self.label

    def adjust_volume(self, y):
        if self.volume_anchor is None:
            self.volume_anchor = y
            self.volume_base = self.control.get_volume()
        dy = y - self.volume_anchor
        if abs(dy) < config.VOLUME_DEADZONE:
            return
        level = self.volume_base - dy * 100 * config.VOLUME_GAIN
        self.control.set_volume(level)
        self.label = "volume " + str(int(min(max(level, 0), 100)))

    def adjust_brightness(self, y):
        if self.brightness_anchor is None:
            self.brightness_anchor = y
            return
        dy = y - self.brightness_anchor
        if abs(dy) >= config.BRIGHTNESS_STEP_DISTANCE:
            self.control.step_brightness(1 if dy < 0 else -1)
            self.brightness_anchor = y
            self.label = "brightness " + ("up" if dy < 0 else "down")