"""
Celery application bootstrap for Influenceur IA
"""

from __future__ import annotations

import os
from celery import Celery


def _make_celery() -> Celery:
    broker_url = os.getenv("CELERY_BROKER_URL", "redis://redis:6379/0")
    result_backend = os.getenv("CELERY_RESULT_BACKEND", "redis://redis:6379/0")

    app = Celery(
        "influenceur_ia",
        broker=broker_url,
        backend=result_backend,
        include=[],  # modules de tâches à ajouter plus tard
    )

    app.conf.update(
        task_default_queue="default",
        task_acks_late=True,
        worker_max_tasks_per_child=100,
        task_ignore_result=False,
        task_serializer="json",
        accept_content=["json"],
        result_serializer="json",
        timezone=os.getenv("TZ", "UTC"),
        enable_utc=True,
    )

    @app.task(name="app.tasks.ping")
    def ping() -> str:  # type: ignore
        return "pong"

    return app


# Celery entrypoint expected by `-A src.app.core.celery_app`
celery_app = _make_celery()


