import json
import queue
import re
import threading
import time

import sounddevice as sd
from vosk import KaldiRecognizer, Model

import config


class VoiceAssistant:
    def __init__(self, control):
        self.control = control
        self.model = Model(config.VOSK_MODEL_PATH)
        self.listening = False
        self.heard = ""
        self.result = ""

    def start_listening(self):
        if self.listening:
            return
        self.listening = True
        self.heard = ""
        self.result = ""
        threading.Thread(target=self.listen, daemon=True).start()

    def listen(self):
        audio = queue.Queue()

        def callback(indata, frames, time_info, status):
            audio.put(bytes(indata))

        recognizer = KaldiRecognizer(self.model, config.VOICE_SAMPLE_RATE)
        deadline = time.monotonic() + config.VOICE_TIMEOUT_SECONDS
        text = ""
        try:
            with sd.RawInputStream(
                samplerate=config.VOICE_SAMPLE_RATE,
                blocksize=4000,
                dtype="int16",
                channels=1,
                callback=callback,
            ):
                while time.monotonic() < deadline:
                    try:
                        data = audio.get(timeout=0.2)
                    except queue.Empty:
                        continue
                    if recognizer.AcceptWaveform(data):
                        text = json.loads(recognizer.Result()).get("text", "")
                        if text:
                            break
                if not text:
                    text = json.loads(recognizer.FinalResult()).get("text", "")
        except Exception:
            self.result = "microphone error"
            self.listening = False
            return
        self.heard = text
        self.result = self.execute(text) if text else "nothing heard"
        self.listening = False

    def execute(self, text):
        text = text.replace("you tube", "youtube").strip()
        play = re.search(r"\bplay (.+)", text)
        if play:
            query = re.sub(r"\s+on youtube$", "", play.group(1)).strip()
            self.control.play_on_youtube(query)
            return "youtube search: " + query
        if "youtube" in text:
            self.control.open_url(config.YOUTUBE_HOME_URL)
            return "open youtube"
        if "volume up" in text:
            self.control.set_volume(self.control.get_volume() + config.VOLUME_VOICE_STEP)
            return "volume up"
        if "volume down" in text:
            self.control.set_volume(self.control.get_volume() - config.VOLUME_VOICE_STEP)
            return "volume down"
        if "mute" in text:
            self.control.set_volume(0)
            return "mute"
        if "brightness up" in text:
            for _ in range(config.BRIGHTNESS_VOICE_STEPS):
                self.control.step_brightness(1)
            return "brightness up"
        if "brightness down" in text:
            for _ in range(config.BRIGHTNESS_VOICE_STEPS):
                self.control.step_brightness(-1)
            return "brightness down"
        for name, app in config.APPS.items():
            if "open " + name in text:
                self.control.open_app(app)
                return "open " + app
        return "unrecognized: " + text