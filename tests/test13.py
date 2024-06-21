import random
import time
import copy
import bisect
from dataclasses import dataclass
from datetime import timedelta, datetime

@dataclass
class Job:
    date: datetime
    title: str
    def __repr__(self) -> str:
        return f"{self.title}: {self.date.strftime("%H:%M:%S")}"
    def __lt__(self, other: 'Job'):
        return self.date < other.date

today = datetime.now()

jobs = [
    Job(today + timedelta(seconds=10), "Play"),
    Job(today + timedelta(seconds=50), "Sleep"),
    Job(today + timedelta(seconds=40), "Eat"),
    Job(today + timedelta(seconds=30), "Work"),
    Job(today + timedelta(seconds=20), "Relax"),
]

jobs.sort(key=lambda item : item.date)
print(jobs)

jobs_map = dict([(job.title, job) for job in jobs])

timers = copy.deepcopy(jobs)
while len(timers) > 0:
    current = datetime.now()
    print(f"{current.strftime("%H:%M:%S")}: {timers}")
    if (timers[0].date <= current):
        deleted_job = timers.pop(0)
        next_job = copy.deepcopy(jobs[random.randint(0, len(jobs) - 1)])
        next_job.date = current + timedelta(seconds=random.randint(1, 10))
        timers.insert(bisect.bisect_left(timers, next_job), next_job)
    time.sleep(1)
