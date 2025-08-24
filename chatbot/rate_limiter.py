# ...existing code from rate_limiter.py...
import time

class TokenBucket:
    def __init__(self, rate, per):
        self.capacity = rate
        self.tokens = rate
        self.per = per
        self.last = time.time()

    def consume(self, tokens=1):
        now = time.time()
        elapsed = now - self.last
        self.last = now
        self.tokens += elapsed * (self.capacity / self.per)
        if self.tokens > self.capacity:
            self.tokens = self.capacity
        if self.tokens >= tokens:
            self.tokens -= tokens
            return True
        return False
