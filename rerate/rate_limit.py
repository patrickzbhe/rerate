from .timestamp_typedef import ts

class RateLimit:
    def __init__(self, count: int = 2, period: ts = 1) -> None:
        '''
        count: number of requests in time period
        period: time period (seconds) 
        '''
        self.count = count
        self.period = period

    @property
    def inverse(self) -> float:
        return self.period / self.count

