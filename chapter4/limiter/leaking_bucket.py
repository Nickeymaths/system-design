import threading
import time
from limiter.rate_limiter import RateLimiter

class LeakingBucket(RateLimiter):
    def __init__(self, bucket_size: int, outflow_rate: int) -> None:
        self.bucket_size = bucket_size
        self.outflow_rate = outflow_rate
        self.current_size = 0
        self.last_out_time = time.time()
        self.lock = threading.Lock()
    
    def process(self):
        while  True:
            ctime = time.time()
            factor = ctime - self.last_out_time
            if factor * self.outflow_rate >= 1:
                if self.current_size >= 1:
                    self.current_size -= 1
                self.last_out_time = ctime
    
    def consume(self) -> bool:
        if self.current_size < self.bucket_size:
            self.current_size += 1
            return True
        
        return False
        
