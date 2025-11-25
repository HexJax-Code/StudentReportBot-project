import redis
from rq import Queue
from app.core.config import settings

redis_conn = redis.from_url(settings.REDIS_URL)
q = Queue("reports", connection=redis_conn)

def enqueue_report_job(student_dict):
    q.enqueue("app.workers.report_worker.process_student", student_dict)
