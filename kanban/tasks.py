import os

from celery import shared_task
from django.utils import timezone
from config.celery import app
from celery.utils.log import get_task_logger

from kanban.models import Tasks

logger = get_task_logger(__name__)


@shared_task()
def check_deadlines():
    now = timezone.now().date()
    tasks = Tasks.objects.filter(deadline__lte=now, deadline_status=False)
    for task in tasks:
        task.deadline_status = True
        task.save()
        logger.info(f'Changed deadline status for task {task.id}')
