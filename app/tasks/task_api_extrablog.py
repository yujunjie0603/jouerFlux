import app.celery_app as celery_app
import time
from celery.utils.log import get_task_logger
from app.models import Firewall
from app.models import Firewall
from flask import g, current_app

logger = get_task_logger(__name__)

@celery_app.celery.task(name='app.celery_app.task_api_extrablog')
def task_api_extrablog(x, y):

    time.sleep(20)
    logger.info(f"=========={x}=======task_api_extrablog========={y}===========")
    return {"result": x + y}

@celery_app.celery.task(name='app.celery_app.send_message_firewall')
def send_message_firewall(id: int):

    firewall = Firewall.query.get(id)
    if firewall:
        logger.info(f"Sending message for firewall: {firewall.name}")
    else:
        logger.warning(f"Firewall not found: {id}")
