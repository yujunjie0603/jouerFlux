from celery import Celery

celery = Celery(
    'jouer_flux',
)
def make_celery(app) -> Celery:

    celery.conf.update(
        broker=app.config["CELERY_BROKER_URL"],
        backend=app.config["CELERY_RESULT_BACKEND"],
        task_serializer="json",
        accept_content=["json"],
        result_serializer="json",
        timezone=app.config.get("TIMEZONE", "Europe/Paris"),
        task_always_eager=app.config.get("CELERY_TASK_ALWAYS_EAGER", False),
        task_acks_late=True,
        task_default_queue = "default",
        worker_prefetch_multiplier=1,
    )
    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)
    celery.Task = ContextTask
    return celery
