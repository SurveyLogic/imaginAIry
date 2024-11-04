NODE_VERSION := 22.8.0

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
	@export NVM_DIR="$$HOME/.nvm"; \
	if [ -s "$$NVM_DIR/nvm.sh" ]; then \
		. "$$NVM_DIR/nvm.sh"; \
		nvm use $(NODE_VERSION) && npm run dev || echo "❌ Failed to start development server. Could not switch to Node.js $(NODE_VERSION). Please install it using: nvm install $(NODE_VERSION)"; \
	else \
		echo "ℹ️  nvm (Node Version Manager) is not installed. Proceeding with system default Node.js version. For version management, consider installing nvm: https://github.com/nvm-sh/nvm#installing-and-updating"; \
		npm run dev; \
	fi

