from .abstract_store import Store
from .exceptions import RateLimitedException 
from .rate_limit import RateLimit
import random
from time import monotonic

from typing import Optional


class DictionaryStore(Store):
    def __init__(self, limit: RateLimit, key: Optional[str]):
        self.limit = limit
        if key is None:
            self.key = str(random.randint(100000, 1000000))
        else:
            self.key = key
        self.d = {}

        self.set_tat(0)


    def get_tat(self):
        return self.d[self.key]

    def set_tat(self, value: str):
        self.d[self.key] = value

    def get_time(self):
        return monotonic()

    def update(self):
        now = self.get_time()
        tat = max(self.get_tat(), now)
        separation = tat - now
        max_interval = self.limit.period - self.limit.inverse
        if separation > max_interval:
            raise RateLimitedException()
        else:
            new_tat = max(tat, now) + self.limit.inverse
            self.set_tat(new_tat)
