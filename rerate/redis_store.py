from redis import Redis 
from .abstract_store import Store 
from .rate_limit import RateLimit
from .exceptions import RateLimitedException
import random

from typing import Optional

LOCK_PREFIX = 'rate_limiter_lock:'

class RedisStore(Store):
    def __init__(
        self,
        limit: RateLimit,
        host: str,
        port: int,
        key: Optional[str],
    ):
        self.limit = limit
        self.r = Redis(host, port)
        if key is None:
            self.key = str(random.randint(100000, 1000000))
        else:
            self.key = key
        print(self.key)

    def get_tat(self):
        return float(self.r.get(self.key))

    def set_tat(self, value: str):
        return self.r.set(self.key, value)

    def get_time(self):
        t = self.r.time()
        return t[0] + t[1] / (10**6)

    def update(self):
        self.r.setnx(self.key, 0)
        now = self.get_time()

        with self.r.lock(f"{LOCK_PREFIX}{self.key}"):
            tat = max(self.get_tat(), now)
            separation = tat - now
            max_interval = self.limit.period - self.limit.inverse
            if separation > max_interval:
                raise RateLimitedException()
            else:
                new_tat = max(tat, now) + self.limit.inverse
                self.set_tat(new_tat)
