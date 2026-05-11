from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class TaskCreateResponse(BaseModel):
    task_id: str
    status: str


class TaskStatusResponse(BaseModel):
    task_id: str
    state: str
    result: str | None = None


class TaskLogResponse(BaseModel):
    id: UUID
    task_id: str
    status: str
    result: str | None
    created_at: datetime
