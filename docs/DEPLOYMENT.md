# Deployment

Instructions on how to deploy this app to Heroku

- [Deployment](#deployment)
  - [Install dependencies](#install-dependencies)
  - [Build](#build)
  - [Add Postgres DB](#add-postgres-db)

## Install dependencies

Make changes in `settings.py` as described [here](https://github.com/TrimHall/sei-flex-django/blob/main/lesson-4.md).

Run `heroku create 90s-shows` to create a heroku app called `90s-shows`

- This adds a new git remote named `heroku`.

Install Heroku buildpacks for poetry and python as described in [this SO reply](https://stackoverflow.com/a/69849137/3210677)

Specify **exact** python version in `pyproject.toml` file. Heroku doesn't accept `^3.9`.

1. Set `python` version to `3.9.12` (released on March 23, 2022) Check [the official python website](https://www.python.org/downloads/) to look up the version numbers of newest releases.
2. Run `poetry update`

## Build

1. Commit your current state
2. Run `git push heroku main` to push the current state of the app to heroku
3. Your should see build output in the console.
   - If one of the last lines is `remote: Verifying deploy... done.` everything was successful.
   - You should see a link to your website.

  ... and see this error:

  <img width="1840" alt="image" src="https://user-images.githubusercontent.com/1945462/163723504-a00081f2-abde-446c-82d8-8ef3279dcd6b.png">

Add URL to `ALLOWED_HOSTS`, i.e. here

```python
ALLOWED_HOSTS = [
    "django-poetry-rest-api.herokuapp.com",
    "0.0.0.0",
]
```

**Attention**: Your URL `https://django-poetry-rest-api.herokuapp.com/` **without** the `https://` part.

## Add Postgres DB

```bash
heroku addons:create heroku-postgresql:hobby-dev
```

Using the `hobby-dev` plan


Copy DB url

postgres://mkrbdivfayzgyd:923afb541b2b2bb686cc0fa900c3ad3cac0e8aa775bb56e8db58db59a293b641@ec2-18-214-134-226.compute-1.amazonaws.com:5432/d7rhnfh3r24fqj

if your local DB name is `90s-baby` and the remote heroku DB is `postgresql-acute-92386`:

```bash
PGUSER= PGPASSWORD= heroku pg:push postgres://localhost/90s-baby postgresql-acute-92386
```

`Procfile`: `web: gunicorn backend.wsgi` where `backend` is your Django project name