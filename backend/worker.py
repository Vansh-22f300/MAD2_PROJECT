from celery import Celery, Task
from flask import Flask

# ✅ Celery Config Class
class CeleryConfig:
    broker_url = 'redis://localhost:6379/0'
    result_backend = 'redis://localhost:6379/1'
    timezone = "Asia/Kolkata"
    enable_utc = True
    beat_schedule = {
        "add-every-10-seconds": {
            "task": "backend.task.daily_reminder",
            "schedule": 10.0
        },
    }

# ✅ FlaskTask must be defined at top-level (not inside a function)
class FlaskTask(Task):
    def __call__(self, *args, **kwargs):
        if not hasattr(self, 'flask_app'):
            raise RuntimeError("Flask app not attached to Celery task")
        with self.flask_app.app_context():
            return self.run(*args, **kwargs)

# ✅ Celery init function
def celery_init_app(app: Flask) -> Celery:
    celery_app = Celery(app.name, task_cls=FlaskTask)
    celery_app.config_from_object(CeleryConfig)
    celery_app.set_default()
    celery_app.Task.flask_app = app  # attach Flask app to task
    app.extensions["celery"] = celery_app
    return celery_app
