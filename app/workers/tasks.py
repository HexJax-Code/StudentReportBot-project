# app/workers/tasks.py
import redis
from rq import Queue
from app.core.config import settings

redis_conn = redis.from_url(settings.REDIS_URL)
q = Queue("reports", connection=redis_conn)

def enqueue_send_job(student_db_id: int, payload: dict = None):
    """
    Enqueue the processing function. We pass payload (e.g., grades) to the worker to avoid
    immediate DB joins in simple flows.
    """
    q.enqueue("app.workers.report_worker.process_and_send", student_db_id, payload, retry=3, result_ttl=5000)
