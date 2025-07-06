from celery_tasks.tasks import matching_task
from task_manager.model import TaskStatus


def test_matching_task(db_instance_empty, session, task1, task2, task3):
    # Write 3 Tasks to DB
    db_instance_empty.create_task(task=task1, session=session)
    db_instance_empty.create_task(task=task2, session=session)
    db_instance_empty.create_task(task=task3, session=session)
    task1.status = TaskStatus.COMPLETED
    tasks = db_instance_empty.read_tasks(session=session)

    assert matching_task(tasks, 2)
    assert matching_task(tasks, 3) == False
    assert matching_task(tasks, 1) == False