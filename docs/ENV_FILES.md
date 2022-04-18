# Make your application safer via an `.env` file

## Install dependency

```bash
poetry add django-environ
```

## `.env` and `.env.example` file

```
DEBUG=True
SECRET_KEY=django-insecure-....
DATABASE_URL=postgres://andru@localhost/90s-baby
```

Add your actual values for `SECRET_KEY` and `DATABASE_URL` after each equals sign.

The `.env.example` file will have this form:

```
# SECURITY WARNING: don't run with the debug turned on in production!
DEBUG=True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY=enter-your-secret-key-here

# Adapt to fit your local username and DB (here it's assumed that there is no DB password)
DATABASE_URL=postgres://<YOUR USER NAME>@localhost/<YOUR DB NAME>
```

## Configure `settings.py`

This is basically following [the official guide](https://django-environ.readthedocs.io/en/latest/getting-started.html).

Add the following to your `settings.py` file:

```python
env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)

# Set the project base directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Take environment variables from .env file
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))
```

Replace hard-coded values with `env()` calls:

1. `DEBUG`:

  ```python
  # False if not in os.environ because of casting above
  DEBUG = env('DEBUG')
  ```

2. `SECRET_KEY`:

    ```python
    SECRET_KEY = env('SECRET_KEY')
    ```

3. Local `DATABASE_URL`:

    ```python
    DATABASES = {
        'default': env.db(),
    }
    ```
