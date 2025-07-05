import pytest
from task_manager.model import TaskStatus
from task_manager.exceptions import TaskNotFoundError


def test_create_and_read_task(db_instance_empty, session, task1):
    """
    Test the creation and reading of a task
    """
    # Write Task to DB
    db_instance_empty.create_task(task=task1, session=session)

    # # Read Task from DB
    task = db_instance_empty.read_task(task_id=1, session=session)
    assert task.status == task1.status
    assert task.validationError == task1.validationError


def test_read_all_tasks(db_instance_empty, session, task1, task2):
    """
    Test the reading of all tasks
    """
    # Write 2 Tasks to DB
    db_instance_empty.create_task(task=task1, session=session)
    db_instance_empty.create_task(task=task2, session=session)

    # Read all Tasks from DB
    tasks = db_instance_empty.read_tasks(session=session)
    assert len(tasks) == 2
    assert tasks[0].status == task1.status
    assert tasks[1].status == task2.status


def test_read_all_tasks_empty(db_instance_empty, session):
    """
    Test the reading of all tasks when the DB is empty
    """
    # Read all Tasks from DB
    tasks = db_instance_empty.read_tasks(session=session)
    assert len(tasks) == 0


def test_delete_task(db_instance_empty, session, task1, task2):
    """
    Test the deletion of a task
    """
    # Write 2 Tasks to DB
    db_instance_empty.create_task(task=task1, session=session)
    db_instance_empty.create_task(task=task2, session=session)

    # Delete Task
    db_instance_empty.delete_task(session=session, task_id=1)

    # Read Task from DB
    with pytest.raises(TaskNotFoundError):
        db_instance_empty.read_task(task_id=1, session=session)


def test_delete_all_tasks(db_instance_empty, session, task1, task2):
    """
    Test the deletion of all tasks
    """
    # Write 2 Tasks to DB
    db_instance_empty.create_task(task=task1, session=session)
    db_instance_empty.create_task(task=task2, session=session)

    # Delete all Tasks from DB
    db_instance_empty.delete_all_tasks(session=session)

    # Read all Tasks from DB
    tasks = db_instance_empty.read_tasks(session=session)
    assert len(tasks) == 0


def test_update_task(db_instance_empty, session, task1):
    """
    Test the updating of a task (status)
    """
    # Write Task to DB
    db_instance_empty.create_task(task=task1, session=session)

    # Update Task
    db_instance_empty.update_task(
        session=session,
        task_id=1,
        task_status=TaskStatus.COMPLETED,
    )

    # Read Task from DB
    task = db_instance_empty.read_task(task_id=1, session=session)

    # Check Task Status and Updated At
    assert task.status == TaskStatus.COMPLETED
    assert task.updated_at > task.created_at

def test_update_task_validation_error(db_instance_empty, session, task1):
    """
    Test the updating of a task (status)
    """
    # Set up fixtures
    validation_error = "Invalid IP range: 192.168.1.256"
    # Write Task to DB
    db_instance_empty.create_task(task=task1, session=session)

    # Update Task
    db_instance_empty.update_task(
        session=session,
        task_id=1,
        task_status=TaskStatus.COMPLETED,
        validation_error=validation_error
    )

    # Read Task from DB
    task = db_instance_empty.read_task(task_id=1, session=session)

    # Check Task Status and Updated At
    assert task.status == TaskStatus.COMPLETED
    assert task.updated_at > task.created_at
    assert task.validation_error == validation_error


def test_update_task_updated_at(db_instance_empty, session, task1):
    """
    Test the updating of a task (updated_at)
    """
    # Write Task to DB
    db_instance_empty.create_task(task=task1, session=session)

    # Update Task
    db_instance_empty.update_task(
        session=session,
        task_id=1,
    )

    # Read Task from DB
    task = db_instance_empty.read_task(task_id=1, session=session)

    # Check Task Updated At is greater than Created At
    assert task.updated_at > task.created_at