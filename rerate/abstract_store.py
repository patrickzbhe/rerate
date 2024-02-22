from abc import ABC, abstractmethod
from .rate_limit import RateLimit
from .exceptions import RateLimitedException


class Store(ABC):
    key: str

    @abstractmethod
    def get_tat(self): ...

    @abstractmethod
    def set_tat(self, value: str): ...

    @abstractmethod
    def get_time(self): ...

    def update(self, limit: RateLimit):
        now = self.get_time()
        tat = max(self.get_tat(self.key), now)
        separation = tat - now
        max_interval = limit.period - limit.inverse
        if separation > max_interval:
            raise RateLimitedException()
        else:
            new_tat = max(tat, now) + limit.inverse
            self.set_tat(self.key, new_tat)
