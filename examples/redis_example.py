from time import sleep
from rerate import RateLimitDecorator, RateLimitedException

limit = RateLimitDecorator(limit=2, period=1, store_option='REDIS', key='my_api_key')

@limit
def example():
    sleep(0.4)
    print('hi')

for _ in range(10000):
    try:
        example()
    except RateLimitedException as e:
        print(e)
