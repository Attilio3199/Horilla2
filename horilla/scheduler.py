"""Safe APScheduler integration for Django database connections.

APScheduler jobs run outside Django's request/response lifecycle.  Without
explicit cleanup, every executor thread can keep a database connection open
for the lifetime of the process.
"""

from functools import wraps

from apscheduler.schedulers.background import BackgroundScheduler as APScheduler
from django.db import close_old_connections, connections


def _run_with_clean_database_connections(job):
    """Run an APScheduler job without retaining its thread-local connection."""

    @wraps(job)
    def wrapped(*args, **kwargs):
        close_old_connections()
        try:
            return job(*args, **kwargs)
        finally:
            connections.close_all()

    return wrapped


class BackgroundScheduler(APScheduler):
    """Background scheduler with bounded workers and Django DB cleanup."""

    def __init__(self, *args, **kwargs):
        # A scheduler is instantiated by several installed apps in every web
        # worker.  One executor thread per scheduler prevents idle database
        # connections from multiplying with APScheduler's default of ten.
        kwargs.setdefault("executors", {"default": {"type": "threadpool", "max_workers": 1}})
        super().__init__(*args, **kwargs)

    def add_job(self, func, *args, **kwargs):
        return super().add_job(_run_with_clean_database_connections(func), *args, **kwargs)
