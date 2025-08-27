from celery import Celery, Task
from celery.schedules import crontab
from flask import Flask

import os # Add this import

class CeleryConfig:
    # Read the Redis URL from Render's environment variables
    redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379')
    broker_url = f"{redis_url}/0"
    result_backend = f"{redis_url}/1"

    timezone = "Asia/Kolkata"
    enable_utc = True
    beat_schedule = {
        "daily-reminder": {
            "task": "backend.task.daily_reminder",
            "schedule": crontab(hour=9, minute=0),
        },
        "monthly-report": {
            "task": "backend.task.send_monthly_report",
            "schedule": crontab(day_of_month=1, hour=9, minute=0),
        }
    }

class FlaskTask(Task):
    def __call__(self, *args, **kwargs):
        if not hasattr(self, 'flask_app'):
            raise RuntimeError("Flask app not attached")
        with self.flask_app.app_context():
            return self.run(*args, **kwargs)


def make_celery(app: Flask):
    celery = Celery(app.import_name, task_cls=FlaskTask)
    celery.config_from_object(CeleryConfig)
    celery.Task.flask_app = app
    app.extensions["celery"] = celery
    return celery
