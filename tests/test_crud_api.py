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
    print(response_json)
    assert response.status_code == 200
    assert response_json["task"]["id"] == create_task_payload["id"]
    assert response_json["task"]["status"] == TaskStatus.NOT_STARTED