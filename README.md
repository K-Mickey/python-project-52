# Task Manager

[![SonarQube Cloud](https://sonarcloud.io/images/project_badges/sonarcloud-light.svg)](https://sonarcloud.io/summary/new_code?id=K-Mickey_python-project-52)

[![Actions Status](https://github.com/K-Mickey/python-project-52/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/K-Mickey/python-project-52/actions)
[![Python CI](https://github.com/K-Mickey/python-project-52/actions/workflows/pyci.yml/badge.svg)](https://github.com/K-Mickey/python-project-52/actions/workflows/pyci.yml)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=K-Mickey_python-project-52&metric=coverage)](https://sonarcloud.io/summary/new_code?id=K-Mickey_python-project-52)

[Description](#description) • [Installation](#installation) • [Usage](#usage) • [Project goals](#project-goals)

## Description

A web application for task management, built using the [Django](https://www.djangoproject.com/) framework. 
It allows users to create, update, and delete tasks, as well as assign them to different statuses.
For working with tasks, users have to register and log in to the application.
The application has an adaptive convenient interface for working with tasks, which is created using [Bootstrap](https://getbootstrap.com/).
As a database, used [PostgreSQL](https://www.postgresql.org/) or [SQLite](https://www.sqlite.org/).
The project is connected to the [Rollbar](https://rollbar.com/) service for error tracking.

This application is deployed on [Render](https://render.com/), so here is [the link](https://github.com/K-Mickey/python-project-52).

### Features

- Protection of important pages from unauthorized access
- All possible actions for managing accounts
- User might create, update and delete any statuses or labels
- Statuses or labels can't be deleted if they have tasks
- Flexible management of tasks
- Only the author of the task can delete it
- Filter tasks by status, executor, label and author
- Translation all pages to different languages
- Powerful default Django admin interface
- Support different databases
- Rollbar service for error tracking

### Requirements

- [Python](https://www.python.org/) 3.14+
- [UV](https://docs.astral.sh/uv/)
- Possibility to run Makefile commands

## Installation

#### Prerequisites

- Make sure you have [Python](https://www.python.org/) installed on your system
- Install [UV](https://docs.astral.sh/uv/) manually if you want to use Makefile commands
- Decide which database to use: [PostgreSQL](https://www.postgresql.org/) or [SQLite](https://www.sqlite.org/)
- Clone the repository and navigate to the project directory:
```bash
git clone https://github.com/K-Mickey/python-project-52.git
cd python-project-52
```

#### Install dependencies

You can just run `build.sh`:
```bash
./build.sh
```
Or you can use Makefile commands:
```bash
make install 
make collectstatic 
make migrate
```
#### Environment variables

Create a `.env` file in the root directory of the project.
Below is an example of such file with default values:
```text
SECRET_KEY=secret_key
DEBUG=False
ALLOWED_HOSTS=127.0.0.1,localhost
DATABASE_URL=sqlite://db.sqlite3
ROLLBAR_ACCESS_TOKEN=access_token
```

Here is an example of variable if you use PostgreSQL:
```text
DATABASE_URL=postgresql://user:password@localhost:5432/db
```

## Usage

You can run the project in development mode:
```bash
make run
```
By default, the project will be available at http://127.0.0.1:8000

And for starting the project in production mode:
```bash
unicorn -b 0.0.0.0:8000 -w 4 task_manager.wsgi
```

If you need to create a superuser, run the command:
```bash
python manage.py createsuperuser
```
After that, you can find the admin interface at http://127.0.0.1:8000/en/admin

### Makefile commands

#### Deployment
- Run build script: `make build`
- Install dependencies: `make install`
- Collect static files: `make collectstatic`
- Create migrations and apply them: `make migrate`
- Command for starting the project at Render: `make render-start`

#### Development
- Create `i18n` locale files with translations: `make make-messages`
- Compile `i18n` locale files: `make compile-messages`
- Lint code: `make lint`
- Format code: `make format`
- Test code: `make test`
- Create coverage report: `make test-coverage`
- Run tests and linter: `make check`
- Run application in development mode: `make run`

## Project goals

The project was created as a part of the [Hexlet](https://ru.hexlet.io/) course.
