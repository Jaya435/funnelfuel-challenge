import time

from task_manager.model import TaskStatus


def test_root(db_instance_empty, test_client):
    response = test_client.get("/api/healthchecker")
    assert response.status_code == 200
    assert response.json() == {"message": "The API is up."}

def test_create_get__task(db_instance_empty, test_client, create_task_payload):
    response = test_client.post("/api/tasks/", json=create_task_payload)
    assert response.status_code == 201

    # Get the created user
    response = test_client.get(f"/api/tasks/{create_task_payload['id']}")
    response_json = response.json()
    assert response.status_code == 200
    assert response_json["task"]["id"] == create_task_payload["id"]
    assert response_json["task"]["status"] == TaskStatus.NOT_STARTED

def test_create_update_task(db_instance_empty, test_client, create_task_payload, task_payload_updated):
    response = test_client.post("/api/tasks/", json=create_task_payload)
    assert response.status_code == 201

    # Update the created user
    time.sleep(
        1
    )  # Sleep for 1 second to ensure updatedAt is different (datetime precision is low in SQLite)
    response = test_client.patch(
        f"/api/tasks/{create_task_payload['id']}", json=task_payload_updated
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

def test_get_task_not_found(test_client):
    response = test_client.get(f"/api/tasks/{9999}")
    assert response.status_code == 404
    response_json = response.json()
    assert response_json["detail"] == f"Task with ID {9999} not found"


def test_create_task_wrong_payload(test_client):
    response = test_client.post("/api/tasks/", json={})
    assert response.status_code == 422


def test_update_task_wrong_payload(test_client, task_payload_updated):
    task_payload_updated["validation_error"] = (
        True  # validation_error should be a string not a boolean
    )
    response = test_client.patch(f"/api/tasks/{2}", json=task_payload_updated)
    assert response.status_code == 422
    response_json = response.json()
    assert response_json == {
        "detail": [
            {
                "type": "string_type",
                "loc": ["body", "validation_error"],
                "msg": "Input should be a valid string",
                "input": True,
            }
        ]
    }


def test_update_user_doesnt_exist(test_client, task_payload_updated):
    response = test_client.patch(f"/api/tasks/3", json=task_payload_updated)
    assert response.status_code == 404
    response_json = response.json()
    assert response_json["detail"] == f"Task with ID {3} not found"