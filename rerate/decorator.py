from typing import Literal, Optional
from .abstract_store import Store
from .dictionary_store import DictionaryStore
from .redis_store import RedisStore
from .rate_limit import RateLimit
from functools import wraps
from .exceptions import BadStoreOption

StoreOption = Literal['REDIS', 'DICTIONARY']

key = None
store_option = 'DICTIONARY'
host = 'localhost' 
port = 6379 

class RateLimitDecorator:
    store: Store
    limit: RateLimit

    def __init__(self, count: int = 15, period: int = 900, store_option: StoreOption = store_option, host: Optional[str] = host, port: Optional[int] = port, key: Optional[str] = key):
        limit = RateLimit(count=count, period=period)
        match store_option:
            case 'DICTIONARY':
                self.dictionary_init(limit, key)
            case 'REDIS':
                self.redis_init(limit, host, port, key)
            case _:
                raise BadStoreOption()
        

    def dictionary_init(self, limit: RateLimit, key: Optional[str]):
        self.store = DictionaryStore(limit, key)

    def redis_init(self, limit: RateLimit, host: str, port: int, key: Optional[str]):
        self.store = RedisStore(limit, host, port, key)

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            self.store.update()
            func(*args, **kwargs)
        
        return wrapper
        


