# Rerate
Flexible ratelimit decorator in Python, with (soon) multiple algorithms and backend stores.

## Installing
```
pip install rerate
```

## Usage
```python
from rerate import limiter
from time import sleep

limit = Limiter(limit=2, period=1, store_option='REDIS', host='localhost', port=6379)

@limit
def example():
    sleep(0.3)
    print('hi')

for _ in range(100):
    try:
        example()
    except Exception:
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