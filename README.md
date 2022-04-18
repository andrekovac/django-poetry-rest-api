# A basic Django REST API

A basic Django REST API with the Django `djangorestframework` (with a 90s music theme)

The JSON response can be accessed via <http://127.0.0.1:8000/api/>

## Run locally

1. Clone the repo.
2. Make sure you have [poetry](https://python-poetry.org/) (python environment and dependency manager) installed.
3. In the project folder run `poetry install` to install dependencies.
4. Run `poetry shell` to open a new shell with all dependencies available.
5. Run `cd backend && python manage.py runserver`
6. Go to <http://127.0.0.1:8000/api/> to view the JSON response

## Links

- Frontend to be deployed on Netlify...
- [Backend](https://django-poetry-rest-api.herokuapp.com/shows/)

## Concepts

### Postgres

See the `DATABASES` entry in `backend/settings.py`

### REST API

- `djangorestframework`
- Data model **serialization** (see `shows/views.py`)

### Connect API to Frontend

- Fetch API data from backend via a React App

## Re-create this project

- [BASIC_POETRY_DJANGO_SETUP.md](./docs/BASIC_POETRY_DJANGO_SETUP.md) contains instructions to set up the basics of this project
- [HOW_TO.md](./docs/HOW_TO.md) contains a step-by-step instruction to recreate this project.

## Further guides

- [DEPLOYMENT.md](./docs/DEPLOYMENT.md): How to deploy this Django project to Heroku
- [ENV_FILES.md](./docs/ENV_FILES.md): How to secure your app in production with an `.env` file
