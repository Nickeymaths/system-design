import time
import threading
from collections import deque
# from limiter.rate_limiter import RateLimiter


class SlidingWindowLogs(object):
    def __init__(self, requests: int, windowTimeInSec: int):
        self.lock = threading.Lock()
        self.timestamps = deque()
        self.requests = requests
        self.windowTimeInSec = windowTimeInSec
    
    def process(self):
        # while True:
        #     pass
        pass

    # eviction of timestamps older than the window time
    def evictOlderTimestamps(self, currentTimestamp):
        while len(self.timestamps) != 0 and (currentTimestamp - 
                self.timestamps[0] > self.windowTimeInSec):
            self.timestamps.popleft()

    # gives current time epoch in seconds
    @classmethod
    def getCurrentTimestampInSec(cls):
        return int(round(time.time()))

    # Checks if the service call should be allowed or not
    def consume(self):
        with self.lock:
            currentTimestamp = self.getCurrentTimestampInSec()
            # remove all the existing older timestamps
            self.evictOlderTimestamps(currentTimestamp)
            self.timestamps.append(currentTimestamp)
            print(len(self.timestamps))
            if len(self.timestamps) > self.requests:
                return False
            return True
