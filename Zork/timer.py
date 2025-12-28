#!/usr/bin/python3

import threading
import time


# Timer-Klasse als Thread
class TimerThread(threading.Thread):
    def __init__(self, update):
        super().__init__()
        self.stop_event = threading.Event()
        self.sekunden_vergangen = 0
        self.update = update

    def run(self):
        while not self.stop_event.is_set():
            stunden, rest = divmod(self.sekunden_vergangen, 3600)
            minuten, sekunden = divmod(rest, 60)
            self.update(f"Current session: {stunden:02}:{minuten:02}:{sekunden:02}")
            time.sleep(1)
            self.sekunden_vergangen += 1

    def stop(self):
        self.stop_event.set()
