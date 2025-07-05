import time

from task_manager.model import TaskStatus


def test_root(db_instance_empty, test_client):
    response = test_client.get("/api/healthchecker")
    assert response.status_code == 200
    assert response.json() == {"message": "The API is up."}

def test_create_get__task(test_client, create_task_payload):
    response = test_client.post("/api/tasks/", json=create_task_payload)
    assert response.status_code == 201

    # Get the created user
    response = test_client.get(f"/api/tasks/{create_task_payload['id']}")
    response_json = response.json()
    assert response.status_code == 200
    assert response_json["task"]["id"] == create_task_payload["id"]
    assert response_json["task"]["status"] == TaskStatus.NOT_STARTED

def test_create_update_task(test_client, create_task_payload, task_payload_updated):
    response = test_client.post("/api/tasks/", json=create_task_payload)
    assert response.status_code == 201

    # Update the created user
    time.sleep(
        1
    )  # Sleep for 1 second to ensure updatedAt is different (datetime precision is low in SQLite)
    response = test_client.patch(
        f"/api/users/{create_task_payload['id']}", json=task_payload_updated
    )
    response_json = response.json()
    assert response.status_code == 202
    assert response_json["task"]["id"] == create_task_payload["id"]
    assert response_json["task"]["status"] == TaskStatus.ERROR
    assert response_json["task"]["validation_error"] == "Invalid IP range: 192.168.1.256"
    assert (
        response_json["task"]["updated_at"] is not None
        and response_json["task"]["updated_at"] > response_json["task"]["created_at"]
    )