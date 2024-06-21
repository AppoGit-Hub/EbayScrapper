import random
import bisect
import time

timers = [20]
"""
for _ in range(0, 10):
    ticks = random.randint(0, 10)
    insertion_index = bisect.bisect_right(timers, ticks)
    timers.insert(insertion_index, ticks)
"""

while len(timers) > 0:
    print(timers)
    timers[0] -= 1
    if (timers[0] <= 0):
        timers.pop(0)
    time.sleep(1)
    if random.randint(0, 3) == 0:  
        timers.append(random.randint(1, 10))