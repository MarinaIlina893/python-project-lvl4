install:
	poetry install

package-install:
	pip install --user dist/*.whl

test:
	poetry run pytest

test-coverage:
	poetry run pytest --cov=task_manager --cov-report xml

lint:
	poetry run flake8 task_manager

selfcheck:
	poetry check

check: selfcheck test lint

build: check
	poetry build

.PHONY: install test lint selfcheck check build