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
	@npm run dev
