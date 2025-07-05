from celery import Celery
from sqlmodel import Session

from celery_config.utils import create_celery
from task_manager.db import DB

celery_app = create_celery()
celery_app.autodiscover_tasks()

@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender: Celery, **kwargs):
    sender.add_periodic_task(10.0, poll_dsp_api.s(), name='Poll DSP every 10 seconds')

@celery_app.task()
def poll_dsp_api():
    print('poll_dsp_api')
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
        print("In here")
        if any(
            dictionary.get("id") == result["id"] for dictionary in tasks
        ):
            db.update_task(session, int(result["id"]), result["status"], result["error_message"])