# FastAPI + Celery + Flower Sample

Minimal Dockerized sample with:
- FastAPI API service
- Celery worker
- Redis as broker and result backend
- PostgreSQL for task persistence
- Flower UI for visual monitoring

## Run

```bash
cp .env.example .env
docker compose up --build
```

## Endpoints

- API docs: http://localhost:8000/docs
- Health: http://localhost:8000/health
- Flower: http://localhost:5555

## Quick test

Create task:

```bash
curl -X POST "http://localhost:8000/tasks/add?x=10&y=32"
```

Get task status:

```bash
curl "http://localhost:8000/tasks/<task_id>"
```

List last 50 logged tasks:

```bash
curl "http://localhost:8000/tasks"
```

Flower docs:
- https://flower.readthedocs.io/en/latest/
