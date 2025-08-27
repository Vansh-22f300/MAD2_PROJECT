from celery import Celery, Task
from celery.schedules import crontab
from flask import Flask


class CeleryConfig:
    broker_url = 'redis://localhost:6379/0'
    result_backend = 'redis://localhost:6379/1'
    timezone = "Asia/Kolkata"
    enable_utc = True
    beat_schedule = {
        "daily-reminder": {
            "task": "backend.task.daily_reminder",
            "schedule": crontab(hour=9, minute=0),  # every day 9 AM
        },
        "monthly-report": {
            "task": "backend.task.send_monthly_report",
            "schedule": crontab(day_of_month=1, hour=9, minute=0),  # 1st of every month
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
