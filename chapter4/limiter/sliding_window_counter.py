import time
import threading
import random
from collections import deque

from .rate_limiter import RateLimiter


class SlidingWindowCount(RateLimiter):
    def __init__(self, requests: int, windowTimeInSec: int):
        self.lock = threading.Lock()
        self.queue = deque()
        self.requests = requests
        self.windowTimeInSec = windowTimeInSec

    # eviction of timestamps older than the window time
    def process(self):
        while True:
            with self.lock:
                if len(self.queue) > 0:
                    ctime = self.getCurrentTimestampInSec()
                    if ctime - self.queue[0] > self.windowTimeInSec:
                        self.queue.popleft()

    # gives current time epoch in seconds
    @classmethod
    def getCurrentTimestampInSec(cls):
        return int(round(time.time()))

    # Checks if the service call should be allowed or not
    def consume(self):
        with self.lock:
            if len(self.queue) < self.requests:
                self.queue.append(self.getCurrentTimestampInSec())
                return True
            return False
