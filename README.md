# FunnelFuel Engineering Challenge

This repository contains a python project that used FastAPI to create an API to create and retrieve tasks and uses
Celery to poll third party APIs to check for task status'

I chose to develop the base API for managing tasks and a polling service to retrieve the status of the task from a third
party API. I did this part first as to me, it was the first building block in deveoloping a rate limited submission
engine. I would need to be able to manage tasks, including retrieving their status from a third party endpoint.

I developed this prototype using Test Driven Development (hopefully that is clear from my commits), and I made sure all
the database endpoints and API operations were tested. This will make this protpotype resilient to changes in the 
future.I used FastAPI as a framework to make my prototype easily extensible. I faced some challenges choosing which 
technology to use for the polling service. I wanted to use a python package that did not have any dependencies. In the
end I chose Celery as it was the easiest to work with and have included Redis, although in a live application I would
prefer to use RabbitMQ.

## Assumptions

1. Tasks that are created using the API have the same ID as the tasks retrieved from the third party APIs
2. The third party API returns an array of objects with a known structure
4. An sqlite3 database is acceptable (although it could be reconfigured for a PostgreSQL DB)

## Getting Started

These instructions will let you get a copy of the project up and running on your local machine for
development and testing purposes. 

### Prerequisites

You will need to run this programme using Python3. You can follow a guide here to install Python3
on your local machine https://installpython3.com/. Once Python3 is installed, you can run this
programme from within a virtual environment.

You will need a message broker to run this application. It defaults to using an instance of redis created with docker
`docker run -d -p 6379:6379 redis`

### Installing

A step by step series of examples that tell you how to get a development env running

Clone the repository onto your local machine
```shell
https://github.com/Jaya435/funnelfuel-challenge.git
```
Create your Python 3 virtual environment, activate it and install all requirements
```shell
pip install -r requirements.txt
```

To run a development web server
```shell
python -m uvicorn task_manager.main:app --reload
```

To run the celery worker and beat scheduler
```shell
celery -A celery_tasks.tasks worker --beat --loglevel=info
```

To perform code formatting
```shell
python -m black .
```
To perform code linting
```shell
python -m ruff check .
```

## Running the tests

The automated tests can be run using the below command:
```shell
pytest
```

## Using the Web Server
Once you have run:
```shell
python -m uvicorn task_manager.main:app --reload
```
The swagger definition can be viewed at:
```shell
http://localhost:8000/docs/
```

## Polling Third Party API
Once you have run:
```shell
python -m uvicorn task_manager.main:app --reload
celery -A celery_tasks.tasks worker --beat --loglevel=info
```
The `celery_tasks/tasks.py` file contains a task that runs every 10 seconds. Currently, the response is mocked and returns an array of three objects:
```shell
[
    {"id": "1", "status": "In Progress"},
    {"id": "2", "status": "Completed"},
    {
        "id": "3",
        "status": "Error",
        "error_message": "Invalid IP range: 192.168.1.256",
    },
]
```
This is to simulate the response from a third party API.
By creating two objects using the `/api/tasks` endpoint that look like this:
```shell
curl --location 'http://localhost:8000/api/tasks' \
--header 'Content-Type: application/json' \
--data '{
  "id": 1,
  "status": "Not Started"
}'
curl --location 'http://localhost:8000/api/tasks' \
--header 'Content-Type: application/json' \
--data '{
  "id": 2,
  "status": "In Progress"
}'
curl --location 'http://localhost:8000/api/tasks' \
--header 'Content-Type: application/json' \
--data '{
  "id": 3,
  "status": "In Progress"
}'
```
The polling task, will update the first task to be in progres, the second task to be completed and the third task to 
be in error with a validation error attached. You can see their status' change using the GET `/api/tasks/{task_id}`
endpoint

## Authors

* **Tom Richmond** - *Initial work* - [Jaya435](https://github.com/Jaya435/)
