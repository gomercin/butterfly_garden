.PHONY: install test lint init
install:
	pip install -e ".[dev]"

test:
	pytest -q

lint:
	ruff check src tests

init:
	butterfly init
