# Detect the shell (sh, bash, etc.)
SHELL := $(shell echo $$SHELL)

# Default target
.DEFAULT_GOAL := help

# Phony targets
.PHONY: help install update run

help:
	@echo "--------------- HELP ---------------"
	@echo "To install frontend dependencies: make install"
	@echo "To update frontend dependencies: make update"
	@echo "To start the frontend server: make run"
	@echo "------------------------------------"

install:
	@npm install

update:
	@npm update

run:
	@if [ -f "$$NVM_DIR/nvm.sh" ]; then \
		. "$$NVM_DIR/nvm.sh" && nvm use 22.8.0 || echo "⚠️ Warning: Unable to switch to Node.js 22.8.0. Continuing with current version."; \
	elif [ -f "$$HOME/.nvm/nvm.sh" ]; then \
		. "$$HOME/.nvm/nvm.sh" && nvm use 22.8.0 || echo "⚠️ Warning: Unable to switch to Node.js 22.8.0. Continuing with current version."; \
	else \
		echo "ℹ️ Note: nvm is not installed or not properly configured. Using system's default Node.js version."; \
	fi
	@npm run dev
