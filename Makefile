# Detect the shell (sh, bash, etc.)
SHELL := $(shell echo $$SHELL)

# Default target
.DEFAULT_GOAL := help

# Variables
BACKEND_DIR := backend
FRONTEND_DIR := frontend

# Phony targets
.PHONY: help venv init-sqlite-db install-be test lint run-be install-fe update-fe run-fe run

help:
	@echo "------------------------ HELP ------------------------"
	@echo "Database:"
	@echo "  init-sqlite-db    Initialize the SQLite database"
	@echo "  init-postgres-db  Initialize the PostgreSQL database"
	@echo "  init-turso-db     Initialize the Turso database"
	@echo ""
	@echo "Backend:"
	@echo "  install-be        Install backend dependencies"
	@echo "  test              Run backend tests"
	@echo "  lint              Run linter on backend code"
	@echo "  run-be            Start the backend development server"
	@echo ""
	@echo "Frontend:"
	@echo "  install-fe        Install frontend dependencies"
	@echo "  update-fe         Update frontend dependencies"
	@echo "  run-fe            Start the frontend development server"
	@echo ""
	@echo "Application:"
	@echo "  run               Run both backend and frontend"
	@echo "------------------------------------------------------"

# Delegate backend-related tasks to backend/Makefile
venv:
	$(MAKE) --no-print-directory -C $(BACKEND_DIR) venv

init-sqlite-db:
	$(MAKE) --no-print-directory -C $(BACKEND_DIR) init-sqlite-db

init-postgres-db:
	$(MAKE) --no-print-directory -C $(BACKEND_DIR) init-postgres-db

init-turso-db:
	$(MAKE) --no-print-directory -C $(BACKEND_DIR) init-turso-db

install-be:
	$(MAKE) --no-print-directory -C $(BACKEND_DIR) install

test:
	$(MAKE) --no-print-directory -C $(BACKEND_DIR) test

lint:
	$(MAKE) --no-print-directory -C $(BACKEND_DIR) lint

run-be:
	$(MAKE) --no-print-directory -C $(BACKEND_DIR) run

# Delegate frontend-related tasks to frontend/Makefile
install-fe:
	$(MAKE) --no-print-directory -C $(FRONTEND_DIR) install

update-fe:
	$(MAKE) --no-print-directory -C $(FRONTEND_DIR) update

run-fe:
	$(MAKE) --no-print-directory -C $(FRONTEND_DIR) run

# Start both backend and frontend
run:
	@echo "Starting backend and frontend..."
	@trap 'kill $(jobs -p)' INT; \
	($(MAKE) run-be 2>&1 | sed 's/^/[BACKEND] /' ) & \
	($(MAKE) run-fe 2>&1 | sed 's/^/[FRONTEND] /' ) & \
	wait
