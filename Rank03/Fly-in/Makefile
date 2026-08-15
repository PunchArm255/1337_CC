PYTHON := python3
PIP := pip3
MAP ?= map.txt

.PHONY: all install run debug clean lint lint-strict

all: run

install:
	$(PIP) install -r requirements.txt

run:
	$(PYTHON) main.py $(MAP)

debug:
	$(PYTHON) -m pdb main.py $(MAP)

clean:
	rm -rf __pycache__ .mypy_cache .pytest_cache *.pyc
	find . -type d -name "__pycache__" -exec rm -rf {} +

lint:
	flake8 . --exclude=backup
	mypy . --exclude backup --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	flake8 . --exclude=backup
	mypy . --exclude backup --strict
