install:
	uv sync --frozen && uv cache prune --ci

collectstatic:
	uv run python manage.py collectstatic --noinput --clear

migrate:
	uv run python manage.py makemigrations
	uv run python manage.py migrate

make-messages:
	django-admin makemessages -l ru

compile-messages:
	django-admin compilemessages
	
build:
	./build.sh

run:
	uv run python manage.py runserver

lint:
	uv run ruff check task_manager --fix

format:
	uv run ruff format .

test:
	uv run python manage.py test

test-coverage:
	uv run coverage run manage.py test
	uv run coverage xml --include="task_manager/*" \
		--omit="*/migrations/*","*/tests/*","task_manager/settings.py"

check: test lint

render-start:
	gunicorn task_manager.wsgi

.PHONY: install collectstatic migrate build lint format test test-coverage check render-start