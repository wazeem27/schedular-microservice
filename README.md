# Scheduler Microservice (FastAPI, Celery, PostgreSQL, Redis)

This project is scheular microservice: implements a scalable microservice for periodic job scheduling. It uses a **Scheduler** built on top of Celery (the distributed task queue).

## Features

1.  **Microservices-based:** Separate containers for API (**FastAPI**), Worker (**Celery Worker**), and Scheduler (**Custom Scheudling **).
2.  **Custom Scheduling:** Celery Beat runs a single, recurring task (`app.tasks.scheduler.check_and_run_jobs`) every 10 seconds. This custom task checks the PostgreSQL DB for jobs where `next_run_at <= NOW()` and launches them dynamically to the workers.
3.  **Tools Used:** FastAPI, Celery, PostgreSQL (DB), Redis (Broker).

## Setup and Installation (Docker Compose)

The recommended way to run this project is using Docker Compose, which mirrors the production environment.

### Prerequisites

* Docker and Docker Compose installed.
* Python 3.12 (for local development/setup).

### 1. Configure Environment

The basic .env is already stored in the root file: So you can just run docker compose up --build to run the system that will bring each services up and running

docker compose up --build -d
3. Verify Running Services
Check that all 5 containers are running healthily:

##### Testing and Verification
1. Access the API
The FastAPI interface is available on your host machine via the exposed port:

Swagger Docs: http://localhost:8000/docs

2. Create a Scheduled Job
Use the Swagger UI (/docs) to POST a new job to /api/v1/jobs.

Example: Schedule a task to append a string into a file

JSON

{
  "name": "Heartbeat-File12-Logge111r",
  "task_name": "app.tasks.jobs.log_heartbeat",
  "schedule_interval": "interval",
  "schedule_params": {
    "minutes": 1
  },
  "task_args": {
    "positional": [
      "my_scheduler_log.txt"
    ],
    "keyword": {}
  }
}
3. Monitor Execution Logs
Watch the combined logs to confirm the custom scheduler is working: or even cna tail -f <filename> (inside the app dir in worker container)

Bash

docker compose logs -f
Beat Logs: Look for the recurring log every 10 seconds: "Custom Scheduler check initiated."

Worker Logs: When the job's next_run_at arrives, the scheduler_worker log will show the task execution: "Task <ID>: Starting number crunching for job ID 1..."

If wanted to run  locally (Alternative):
Create a virtual env and pip install the requirement
Then follow the below Makefile targets to run it individually

Start dependencies and initialize the DB:

Bash

make local-setup
Run the services in separate terminals:

Bash

# Terminal 1: FastAPI API
make api

# Terminal 2: Celery Worker
make worker

# Terminal 3: Celery Beat (The Custom Scheduler)
make beat
Stop local dependencies:

Bash

make local-down