from fastapi import Depends, FastAPI
from sqlalchemy import desc, select
from sqlalchemy.orm import Session

from app.celery_app import celery_app
from app.config import settings
from app.db import Base, SessionLocal, engine
from app.models import TaskLog
from app.schemas import TaskCreateResponse, TaskLogResponse, TaskStatusResponse
from app.tasks import add

app = FastAPI(title=settings.project_name)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.on_event("startup")
def startup() -> None:
    Base.metadata.create_all(bind=engine)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/tasks/add", response_model=TaskCreateResponse)
def enqueue_add(x: int, y: int, db: Session = Depends(get_db)) -> TaskCreateResponse:
    task = add.delay(x, y)
    db.add(TaskLog(task_id=task.id, status="PENDING", result=None))
    db.commit()
    return TaskCreateResponse(task_id=task.id, status="PENDING")


@app.get("/tasks/{task_id}", response_model=TaskStatusResponse)
def task_status(task_id: str, db: Session = Depends(get_db)) -> TaskStatusResponse:
    celery_result = celery_app.AsyncResult(task_id)
    result_value = None
    if celery_result.ready() and celery_result.result is not None:
        result_value = str(celery_result.result)
    item = db.scalar(select(TaskLog).where(TaskLog.task_id == task_id))
    if item is not None:
        item.status = celery_result.state
        item.result = result_value or item.result
        db.commit()
    return TaskStatusResponse(
        task_id=task_id,
        state=celery_result.state,
        result=result_value,
    )


@app.get("/tasks", response_model=list[TaskLogResponse])
def list_tasks(db: Session = Depends(get_db)) -> list[TaskLogResponse]:
    items = db.scalars(select(TaskLog).order_by(desc(TaskLog.created_at)).limit(50)).all()
    return [
        TaskLogResponse(
            id=item.id,
            task_id=item.task_id,
            status=item.status,
            result=item.result,
            created_at=item.created_at,
        )
        for item in items
    ]
