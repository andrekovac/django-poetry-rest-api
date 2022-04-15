## Django REST API

- [Django REST API](#django-rest-api)
  - [Postgres: Switch DB engine from SQLite to Postgres](#postgres-switch-db-engine-from-sqlite-to-postgres)
  - [Create a basic Django App](#create-a-basic-django-app)
  - [New App `shows`](#new-app-shows)
- [Build a REST API](#build-a-rest-api)
  - [`djangorestframework`](#djangorestframework)
  - [Serializer](#serializer)

### Postgres: Switch DB engine from SQLite to Postgres

1. `poetry add psycopg2`
2. Create new Postgres DB via **TablePlus** (or via `createdb 90s-baby` or inside of `psql`)

    <img width="455" alt="image" src="https://user-images.githubusercontent.com/1945462/163567032-408cce71-6c26-49d3-8997-264bdd476836.png">

3. In `backend/settings.py` replace `DATABASES` entry with:

    ```python
    # added this to use postgres as the databse instead of the default sqlite.
    # do this before running the initial migrations or you will need to do it again.
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': '90s-baby',
            'HOST': 'localhost',
            'PORT': 5432
        }
    }
    ```

    **Note**: Name `90s-baby` has to match!

    See [the official documentation](https://docs.djangoproject.com/en/4.0/ref/settings/#databases)

4. Run `python manage.py migrate`
5. Check out the database tables in **TablePlus**

### Create a basic Django App

Follow steps in [BASIC_POETRY_DJANGO_SETUP.md](./BASIC_POETRY_DJANGO_SETUP.md)

### New App `shows`

Create a Django app `shows` and create some entries via the Django Admin panel.

This is equivalent to the app `books` in the [django-poetry-admin-model](https://github.com/andrekovac/django-poetry-admin-model) app.

- Follow the [HOW-TO instructions in the django-poetry-admin-model project](https://github.com/andrekovac/django-poetry-admin-model/blob/main/docs/HOW_TO.md) for more in-detail explanations.

Here the rough steps:

1. `django-admin startapp shows`
2. Create `show` model (see `shows/models.py`)

    ```python
    class Show(models.Model):
        title = models.CharField(max_length=40, unique=True)
        album_name = models.CharField(max_length=60)
        duration = models.FloatField()
        year = models.FloatField()
        artist = models.CharField(max_length=50)
        created = models.DateTimeField(auto_now_add=True)

        def __str__(self):
            return f'{self.title} - {self.artist}'
    ```

3. In `backend/settings.py` add `shows` to `INSTALLED_APPS`
4. Connect the `Show` model to the admin panel in `shows/admin.py` via `admin.site.register(Show)`
5. Make migrations (`python manage.py makemigrations`) and run migration (`python manage.py migrate`)
6. Create a super user (`python manage.py createsuperuser`), start the server (`python manage.py runserver`) and login into the Admin panel
7. Create a TV show and observe it in **TablePlus**

## Build a REST API

### `djangorestframework`

1. Add dependency `djangorestframework` via `poetry add djangorestframework`
2. Register it in `backend/settings.py` by adding `'rest_framework'` to `INSTALLED_APPS`


### Serializer

Here we define the model the JSON will be using and specify which fields to look at.

1. Create a new file `serializers.py`

    ```python
    from rest_framework import serializers
    from .models import Show

    class ShowSerializer(serializers.ModelSerializer):
        class Meta: 
            model = Show
            fields = '__all__'
    ```

2. Let's adapt `shows/views.py`:

    Class-based approach:

    ```python
    from rest_framework.views import APIView
    from rest_framework.response import Response 

    from .models import Show
    from .serializers import ShowSerializer

    class ShowListView(APIView):

        def get(self, _request):
            shows = Show.objects.all()
            serialized_shows = ShowSerializer(shows, many=True)
            return Response(serialized_shows.data)    
    ```

    There's also a functional approach which works with decorators.