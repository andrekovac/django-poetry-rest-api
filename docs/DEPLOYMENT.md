# Deployment

Instructions on how to deploy this Django app to Heroku

- [Deployment](#deployment)
  - [Install dependencies](#install-dependencies)
  - [Create heroku app](#create-heroku-app)
  - [Heroku & Poetry compatibility](#heroku--poetry-compatibility)
  - [Configuration in `settings.py`](#configuration-in-settingspy)
  - [Heroku Procfile](#heroku-procfile)
  - [Build](#build)
  - [Database](#database)
    - [Sync your local DB with remote DB](#sync-your-local-db-with-remote-db)
  - [Set two more heroku config variables](#set-two-more-heroku-config-variables)
  - [Commit + push](#commit--push)
  - [Increase secruity with `.env` files](#increase-secruity-with-env-files)

## Install dependencies

Run the following command in the project folder:

```bash
poetry add dj_database_url gunicorn whitenoise
```

This will install dependencies `dj_database_url`, `gunicorn` and `whitenoise`.

## Create heroku app

If you haven't already, you'll need to set up Heroku.

1. Sign up for an account at [heroku.com](https://heroku.com)
2. Install the heroku CLI
   
   ```sh
   brew install heroku/brew/heroku
   ```
3. Login on the CLI
   
   ```sh
   heroku login
   ```
   and follow the instructions to login via your browser.

With all that done, you're ready to create your heroku app for this project.

```sh
heroku create <your-app-name>
```

will create the app for you (among other things it will create a new git remote named `heroku`).
If you don't provide a name, heroku will give it a random one. I picked `90s-shows`, so I executed `heroku create 90s-shows`

You can view your heroku apps from the command line with `heroku apps` or by going to the [Heroku dashboard](https://dashboard.heroku.com/).
## Heroku & Poetry compatibility

1. In order to support **poetry**, we need to replace the heroku buildpacks. To do so, run the following three commands (taken from [this SO reply](https://stackoverflow.com/a/69849137/3210677)):

  ```sh
  heroku buildpacks:clear
  heroku buildpacks:add https://github.com/moneymeets/python-poetry-buildpack.git
  heroku buildpacks:add heroku/python
  ```

2. Specify **exact** python version in `pyproject.toml` file. Heroku doesn't accept `^3.9`.

   1. Set `python` version to `3.9.12` (released on March 23, 2022). Check [the official python website](https://www.python.org/downloads/) to look up the version numbers of newest releases.
   2. Run `poetry update`

## Configuration in `settings.py`

1. Right after the `STATIC_URL` value, add the following:

  ```python
  # Location where django collect all static files
  STATIC_ROOT = os.path.join(BASE_DIR, "static")

  STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
  ```

2. Replace the `DATABASES` entry with the following:

  ```python
  DATABASES = {
      'default': dj_database_url.config(
          default='postgres://andru@localhost/90s-baby', conn_max_age=600
      )
  }
  ```

3. Change `ALLOWED_HOSTS` to:

  ```python
  ALLOWED_HOSTS = ["django-poetry-rest-api.herokuapp.com",
                 "localhost", "127.0.0.1"]
  ```
  
  where you replace `django-poetry-rest-api.herokuapp.com` with your heroku app. **Attention**: It's your URL `https://django-poetry-rest-api.herokuapp.com/` **without** the `https://` part.

4. `MIDDLEWARE`

  Django also doesn't support production fileserving, so to cover this, we have some whitenoise settings to add.

  Add this as last entry in `MIDDLEWARE`:

  ```python
  MIDDLEWARE = [
      ...,
      # Simplified static file serving: https://warehouse.python.org/project/whitenoise/
      "whitenoise.middleware.WhiteNoiseMiddleware",
  ]
  ```

## Heroku Procfile

1. Create a file called `Procfile`.
2. It's content: `web: gunicorn backend.wsgi` where `backend` is your Django project name (in case it's not `backend`)

This file tells heroku which command to run as soon as everything is uploaded and deployed.

## Build

1. Commit your current state (e.g. `git add -A && commit -m "deployment"`)
2. Run `git push heroku main` to push the current state of the app to heroku
3. Your should see build output in the console.
   - If one of the last lines is `remote: Verifying deploy... done.` everything was successful.
   - You should see a link to your website.

  ... and see this error (or something similar):

  <img width="1840" alt="image" src="https://user-images.githubusercontent.com/1945462/163723504-a00081f2-abde-446c-82d8-8ef3279dcd6b.png">

## Database

A databse should have been automatically created for you. To check whether it did, look at the heroku dashboard.
If you see a DB dyno there, the database was created for you. If there is no dyno, then run the following command:

```bash
heroku addons:create heroku-postgresql:hobby-dev
```

- **Note**: `hobby-dev` describes the free heroku plan

### Sync your local DB with remote DB

1. Run `heroku pg:info` to get information about your Heroku database in the cloud
2. The last line will contain your heroku DB name (e.g. `postgresql-acute-92386`). You'll need this name in a second
3. Note down your local DB name (check it out in e.g. **TablePlus**)
4. With my local DB name `90s-baby` and the remote heroku DB name `postgresql-acute-92386` I ran:

```bash
PGUSER= PGPASSWORD= heroku pg:push postgres://localhost/90s-baby postgresql-acute-92386
```

Run the same command but just replace `90s-baby` and `postgresql-acute-92386` with your values.

## Set two more heroku config variables

1. `ALLOWED_HOSTS`
   
   Change `django-poetry-rest-api` with your app name

  ```bash
  heroku config:set ALLOWED_HOSTS=django-poetry-rest-api.herokuapp.com
  ```

2. `SECRET_KEY`

  Change `DJANGO_SECRET_KEY` with your actual `SECRET_KEY` value:

  ```bash
  heroku config:set SECRET_KEY=DJANGO_SECRET_KEY
  ```

  (**Side note**: You can create a new secret key with `python -c "import secrets; print(secrets.token_urlsafe())"`. Make sure that you then update the `SECRET_KEY` value in `settings.py` as well as the Heroku config value `SECRET_KEY`)

Partly taken from [this guide](https://dev.to/mdrhmn/deploying-django-web-app-using-heroku-updated-1fp).

## Commit + push

A commit to the `main` branch of the git `heroku` remote will trigger a new deployment:

1. Commit your current state
  
  ```bash
  git add -A && commit -m "finalize deployment"
  ```

2. Push to the `main` branch on the remote named `heroku` (not `origin` this time): 
  ```bash
  git push heroku main
  ```

3. You should see heroku churning through a deployment. If everything was successful, open the link which is shown at the end of the output to view it in the browser.

4. Test whether your requests work in **Insomnia** or **Postman** or via your Frontend App.

## Increase secruity with `.env` files

Follow the guide [ENV_FILES.md](./ENV_FILES.md) to increase the security of your deployed app.
