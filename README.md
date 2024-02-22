# Rerate
Flexible rate limiter in Python, with (soon) multiple algorithms and backend stores.

## Installing
```
pip install rerate
```

## Usage
```python
from rerate import limiter, RateLimitedException
from time import sleep

limit = Limiter(limit=2, period=1, store_option='REDIS', host='localhost', port=6379)

@limit
def example():
    sleep(0.3)
    print('hi')

for _ in range(100):
    try:
        example()
    except RateLimitedException as e:
        print('I got limited!')
```

## Supported Storage Options
- Redis
- Local (dictionary)

## Supported Algorithms
- Generic Cell Rate

## Todo
- More backends, more algorithms
- Better exceptions
- Built in retry
- Async

## Acknowledgments
A lot of the ideas/code is inspired by:
- https://engineering.ramp.com/rate-limiting-with-redis
- https://smarketshq.com/implementing-gcra-in-python-5df1f11aaa96
- https://github.com/tomasbasham/ratelimit
