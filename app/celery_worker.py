from celery import Celery
from app import create_app
from app.celery_app import make_celery

flask_app = create_app()
celery = make_celery(flask_app)
