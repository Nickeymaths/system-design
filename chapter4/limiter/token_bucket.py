import time
import threading
from .rate_limiter import RateLimiter

class TokenBucket(RateLimiter):
    def __init__(self, capacity: int, refill_rate: int):
        self.capacity = capacity
        self.refill_rate = refill_rate
        self.number_of_tokens = capacity
        self.last_fill_time = time.time()
        self.lock = threading.Lock()
        
    def process(self):
        self.last_fill_time = time.time()
        while True:
            time.sleep(1/self.refill_rate)
            self.fill_bucket()
    
    def fill_bucket(self):
        ctime = time.time()
        factor = ctime - self.last_fill_time
        with self.lock:
            self.number_of_tokens = min(self.capacity, self.number_of_tokens + factor*self.refill_rate)
        self.last_fill_time = ctime
    
    def consume(self) -> bool:
        with self.lock:
            if self.number_of_tokens >= 1:
                self.number_of_tokens -= 1
                return True
        return False
