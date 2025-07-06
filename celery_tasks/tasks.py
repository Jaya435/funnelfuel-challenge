from celery import Celery
from celery.utils.log import get_task_logger
from sqlmodel import Session

from celery_config.utils import create_celery
from task_manager.db import DB
from task_manager.model import TaskStatus

celery_app = create_celery()
celery_app.autodiscover_tasks()
logger = get_task_logger(__name__)

@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender: Celery, **kwargs):
    sender.add_periodic_task(10.0, poll_dsp_api.s(), name='Poll DSP every 10 seconds')


def matching_task(tasks, result_id):
    for task in tasks:
        if task.id == result_id and (task.status == TaskStatus.IN_PROGRESS or task.status == TaskStatus.NOT_STARTED):
            return True
    return False


@celery_app.task()
def poll_dsp_api():
    db = DB()
    session = Session(db.engine)
    response = [
            {
                "id": "1",
                "status": "In Progress"
            },
            {
                "id": "2",
                "status": "Completed"
            },
            {
                "id": "3",
                "status": "Error",
                "error_message": "Invalid IP range: 192.168.1.256"
            }
        ]
    tasks = db.read_tasks(session)
    for result in response:
        result_id = int(result["id"])
        if matching_task(tasks, result_id):
            logger.info(f"Updating task: `{result_id}`")
            db.update_task(
                session, result_id, result["status"], result["error_message"] if "error_message" in result else None
            )