SHELL:=/bin/bash

APP_PATH                := src
VENV_PATH               := .venv
VENV_NAME               := "gipoc"
BUILD_PATH              := build
ARCHIVE_NAME    := gipoc.zip

EXCLUDED_FILES := __init__.py

.PHONY: format
format:
	 isort . && black --preview --config pyproject.toml src tests

.PHONY: lint

lint:
	pylint --ignore=$(EXCLUDED_FILES) src || true

.PHONY: setup

setup:
	( \
		python -m venv --prompt $(VENV_NAME) $(VENV_PATH); \
		source $(VENV_PATH)/bin/activate \
		&& python -m pip install --upgrade pip \
		&& python -m pip install -r requirements.build.txt ; \
	    )
