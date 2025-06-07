import time
import threading
from collections import deque

from .rate_limiter import RateLimiter


class SlidingWindowLogs(RateLimiter):
    def __init__(self, requests: int, windowTimeInSec: int):
        self.lock = threading.Lock()
        self.timestamps = deque()
        self.requests = requests
        self.windowTimeInSec = windowTimeInSec
    
    def process(self):
        while True:
            self.evictOlderTimestamps()

    # eviction of timestamps older than the window time
    def evictOlderTimestamps(self):
        currentTimestamp = self.getCurrentTimestampInSec()
        while len(self.timestamps) > 0 and (currentTimestamp - 
                self.timestamps[0] > self.windowTimeInSec):
            self.timestamps.popleft()

    # gives current time epoch in seconds
    @classmethod
    def getCurrentTimestampInSec(cls):
        return int(round(time.time()))

    # Checks if the service call should be allowed or not
    def consume(self):
        with self.lock:
            self.timestamps.append(self.getCurrentTimestampInSec())
            if len(self.timestamps) > self.requests:
                return False
            return True
