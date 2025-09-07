# Makefile for building Python packages with uv and running unittests

.PHONY: all install test coverage clean

PYTHON ?= python3
UV ?= uv

all: install test

sync:
	$(UV) sync

install:
	$(UV) build

test:
	$(UV) run $(PYTHON) -m pytest -v -s test

coverage:
	$(UV) run $(PYTHON) -m pytest --cov=. --cov-report=term-missing -v -s test

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +