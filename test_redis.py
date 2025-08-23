from redis import Redis
import rq
from app.tasks import example 

# queue = rq.Queue('microblog-tasks', connection=Redis.from_url('redis://'))
# job = queue.enqueue('app.tasks.example', 23)
# print(job.get_id())
# print(job.is_finished)


# >>> job = queue.enqueue('app.tasks.example', 23)
# >>> job.meta
# {}
# >>> job.refresh()
# >>> job.meta
# {'progress': 13.043478260869565}
# >>> job.refresh()
# >>> job.meta
# {'progress': 69.56521739130434}
# >>> job.refresh()
# >>> job.meta
# {'progress': 100}
# >>> job.is_finished
# True


# app/tasks.py

queue = rq.Queue('microblog-tasks', connection=Redis.from_url('redis://'))
job = queue.enqueue('example', 23)

while not job.is_finished:
    job.refresh()
    print(job.meta.get('progress', 0), '%')