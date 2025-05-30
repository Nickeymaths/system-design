from abc import ABC, abstractmethod

class RateLimiter:
    @abstractmethod
    def process(self):
        pass
    
    @abstractmethod
    def consume(self) -> bool:
        pass
