# Scheduler Microservice Setup Guide

This document provides step-by-step instructions for setting up and running the Scheduler Microservice project using Docker Compose, followed by an alternative local setup guide.

---

## 🚀 1. Project Overview

This project implements a scalable microservice for periodic job scheduling using a decoupled, microservices-based architecture.

* **API:** FastAPI (Handles job creation and retrieval)
* **Task Queue:** Celery
* **Database:** PostgreSQL (Stores job configurations, run history)
* **Message Broker:** Redis
* **Custom Scheduling Logic:** Celery Beat executes a periodic task (`app.tasks.scheduler.check_and_run_jobs`) that polls the PostgreSQL database to identify and launch jobs that are due (`next_run_at <= NOW()`).

---

## 🛠️ 2. Setup and Installation (Docker Compose - Recommended)

The recommended method uses Docker Compose, which mirrors the production environment by running separate containers for the API, Worker, Beat, Database, and Redis.

### Prerequisites

* Docker and Docker Compose installed on your system.

### Step 1: Configure Environment

The project requires a basic `.env` file for database and broker configuration.

* Ensure a `.env` file exists in the project root directory (mirrored from `.env.example`).
* If you need to update variables, edit the `.env` file.

### Step 2: Build and Launch Services

Run the following command from the project root directory. The services are configured with health checks and dependencies to ensure correct startup order.

```bash
docker compose up --build -d
```

### Step 3: Verify Running Services

Check the status of all five containers. They should all be in a healthy state:

```bash
docker compose ps
```

You should see:

* `scheduler_api`
* `scheduler_worker`
* `scheduler_beat`
* `postgres_db`
* `redis_broker`

all running.

---

## ✅ 3. Testing and Verification

### Step 1: Access the API Documentation

The FastAPI interface exposes the Swagger UI for testing the job creation endpoint.

* **Swagger Docs URL:** [http://localhost:8000/docs](http://localhost:8000/docs)

### Step 2: Create a Scheduled Job

Use the Swagger UI to execute a POST request to the `/v1/jobs` endpoint to create your first scheduled job.

**Example Payload:** Schedule the `log_heartbeat` task to run every minute.

```json
{
  "name": "Heartbeat-File-Logger",
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
```

### Step 3: Monitor Execution Logs

Monitor the combined container logs in real-time to confirm that the custom scheduler and worker are functioning correctly.

```bash
docker compose logs -f
```

* **Beat Logs:** Look for the log indicating the periodic check (e.g., `"Custom Scheduler check initiated."` every 10 seconds).
* **Worker Logs:** When the job's calculated `next_run_at` is reached, the `scheduler_worker` will log the task execution (e.g., `"Task <ID>: Successfully logged heartbeat to..."`).
* **File Verification:** To confirm the file was written, you can exec into the worker container:

```bash
docker exec -it scheduler_worker /bin/bash
cat my_scheduler_log.txt 
exit
```

---

## 🖥️ 4. Local Setup (Alternative)

If you prefer to run the API, Worker, and Beat directly on your host machine for debugging purposes:

### Prerequisites (Local)

* Python 3.12 installed
* PostgreSQL and Redis running (handled by Docker Compose in Step 1 below)

### Step 1: Prepare Dependencies and Environment

Start only the dependent services (Database and Redis) and initialize the DB.

```bash
# Start PostgreSQL and Redis containers only
docker compose up db redis -d

# Initialize the DB (assuming 'make local-setup' runs migrations)
make local-setup
```

### Step 2: Install Python Requirements

Create and activate a virtual environment, then install all dependencies.

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Step 3: Run Services Individually

Open three separate terminal windows and run the following Makefile targets:

* **Terminal 1: FastAPI API**

```bash
make api
```

* **Terminal 2: Celery Worker**

```bash
make worker
```

* **Terminal 3: Celery Beat (The Custom Scheduler)**

```bash
make beat
```

### Step 4: Stop Local Dependencies

Once finished, stop the PostgreSQL and Redis containers started in Step 1.

```bash
make local-down
```
