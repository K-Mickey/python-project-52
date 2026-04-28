install:
	uv sync --frozen && uv cache prune --ci

collectstatic:
	uv run python task_manager/manage.py collectstatic

makemigrations:
	uv run python task_manager/manage.py makemigrations

migrate:
	uv run python task_manager/manage.py migrate

build:
	./build.sh

run:
	uv run python task_manager/manage.py runserver

lint:
	uv run ruff check task_manager --fix

format:
	uv run ruff format .

test:
	uv run pytest

test-coverage:
	uv run pytest --cov=task_manager --cov-report xml

check: test lint

render-start:
	gunicorn task_manager.wsgi

.PHONY: install collectstatic makemigrations migrate build lint format test test-coverage check render-start