from celery.utils.log import get_task_logger
from sqlalchemy import select

from app.celery_app import celery_app
from app.db import Base, SessionLocal, engine
from app.models import TaskLog

logger = get_task_logger(__name__)
Base.metadata.create_all(bind=engine)


@celery_app.task(name="tasks.add")
def add(x: int, y: int) -> int:
    task_id = add.request.id
    result = x + y
    with SessionLocal() as db:
        item = db.scalar(select(TaskLog).where(TaskLog.task_id == task_id))
        if item is None:
            item = TaskLog(task_id=task_id, status="SUCCESS", result=str(result))
            db.add(item)
        else:
            item.status = "SUCCESS"
            item.result = str(result)
        db.commit()
    logger.info("Task %s finished with result=%s", task_id, result)
    return result
