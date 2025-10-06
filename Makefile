.PHONY: build up down api worker beat setup clean logs

COMPOSE_FILE = docker-compose.yml
COMPOSE_LOCAL_FILE = docker-compose.local.yml


local-up:
	@echo "Starting local dependencies (Postgres & Redis containers)..."
	docker compose -f $(COMPOSE_LOCAL_FILE) up -d db redis

local-down:
	@echo "Stopping local dependencies..."
	docker compose -f $(COMPOSE_LOCAL_FILE) down -v

local-setup: local-up
	@echo "Running local DB setup (SQLAlchemy create_all)..."
	# Ensure dependencies are available before running python setup
	sleep 5
	# FIX: Execute app.main.py to run Base.metadata.create_all()
	python3 -c "import app.main"


api:
	@echo "Starting FastAPI API Server (Local)..."
	uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

worker:
	@echo "Starting Celery Worker (Local)..."
	celery -A app.tasks worker -l INFO

beat:
	@echo "Starting Scheduler heart beat (Local) for CUSTOM scheduling..."
	celery -A app.tasks beat -l INFO

clean: cleanup-pyc cleanup-logs
	@echo "Project cleaned."

cleanup-pyc:
	@echo "Removing Python cache files (.pyc, __pycache__, .pytest_cache)..."
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf .pytest_cache

cleanup-logs:
	@echo "Removing volume-mounted log files..."
	rm -rf logs/*