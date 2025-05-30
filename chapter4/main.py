import os
import time
import threading
from datetime import datetime
import uuid

from matplotlib import pyplot as plt
import pandas as pd
from limiter.rate_limiter import RateLimiter
from limiter.token_bucket import TokenBucket

class Runner:
    def __init__(self, rps: int, rate_limiter: RateLimiter, duration: int) -> None:
        self.rps = rps
        self.rate_limiter = rate_limiter
        self.duration = duration
        self.counter = []
        self._limiter_thread = threading.Thread(target=self.rate_limiter.process)
        self._runner_thread = threading.Thread(target=self._run)
        
    def _run(self):
        start_time = time.time()
        while time.time() - start_time < self.duration:
            time.sleep(1/self.rps)
            self.counter.append((str(datetime.now()), self.rate_limiter.consume()))
        
        self.export_result()
    
    def export_result(self):
        id = str(uuid.uuid4())
        df = pd.DataFrame(self.counter, columns=['timestamp', 'accepted'])
        os.makedirs("output", exist_ok=True)
        df.to_csv(f"output/{id}.csv", index=False)
        self.save_image(id, df)
    
    def save_image(self, image_name: str, result: pd.DataFrame):
        result["timestamp"] = pd.to_datetime(result["timestamp"])
        result["accepted"] = result["accepted"].astype(int)
        result.set_index("timestamp", inplace=True)
        result.sort_index(inplace=True)
        
        grouped_by_timeframe = result.resample('1s').sum()
        fig, ax = plt.subplots()
        ax.plot(grouped_by_timeframe.index, grouped_by_timeframe["accepted"], marker='o')
        ax.set_title(f"Accepted over Time of {self.rate_limiter.__class__.__name__}")
        ax.set_xlabel("Timestamp")
        ax.set_ylabel("Accepted Count")
        fig.autofmt_xdate()

        fig.savefig(f"output/{image_name}.png")
    
    def start(self):
        self._limiter_thread.start()
        time.sleep(10)
        self._runner_thread.start()


if __name__ == '__main__':
    rps = 20
    rate_limiter = TokenBucket(capacity=10, refill_rate=10)
    duration = 30
    
    runner = Runner(rps, rate_limiter, duration)
    runner.start()
