## Django REST API

- [Django REST API](#django-rest-api)
  - [Postgres: Switch DB engine from SQLite to Postgres](#postgres-switch-db-engine-from-sqlite-to-postgres)
  - [Create a basic Django App](#create-a-basic-django-app)
  - [New App `shows`](#new-app-shows)
- [Build a REST API](#build-a-rest-api)
  - [`djangorestframework`](#djangorestframework)
  - [Serializer](#serializer)
  - [Add a view to list all shows](#add-a-view-to-list-all-shows)
  - [Add a second view to retrieve a particular show](#add-a-second-view-to-retrieve-a-particular-show)
- [Oh no! We forgot a field in the database!](#oh-no-we-forgot-a-field-in-the-database)
- [React Client App](#react-client-app)
  - [CORS](#cors)

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

- Follow the [HOW-TO instructions in the django-poetry-admin-model project](https://github.com/andrekovac/django-poetry-admin-model/blob/main/docs/HOW_TO.md) for more in-detail explanations on how to create a new Django app in general. 

Here the rough steps to create a new `shows` app:

1. `django-admin startapp shows`
2. Create `show` model (see `shows/models.py`)

    ```python
    from django.db import models


    class Show(models.Model):
        """
        A 90s TV show
        """
        title = models.CharField(
            max_length=50, default=None)  # fields are required by default so no need to specify
        image = models.CharField(max_length=50, default=None)

        # must be positive number, integerfield can be negative
        year = models.PositiveIntegerField(default=None)
        worth_a_watch = models.BooleanField(default=True, null=True)

        def __str__(self):
            """Formats entries in the Admin panel"""
            return f"{self.title} - {self.year}"
    ```

3. In `backend/settings.py` add `shows` to `INSTALLED_APPS`
4. Connect the `Show` model to the admin panel:

   1. In `shows/admin.py` add the line `admin.site.register(Show)`
   2. Hover over `Show` with your cursor and hit `Cmd + .` -> pick the import from `shows.models` -> This should create `from shows.models import Show`

5. Make migrations (`python manage.py makemigrations`) and run migration (`python manage.py migrate`)
6. Create a super user (`python manage.py createsuperuser`). Just use `admin` as username and password. Yes, let's bypass password validation 🙈
7. Start the server (with `python manage.py runserver`) and login into the Admin panel
8. Create a few TV shows
9. Observe in **TablePlus** that new rows got created.

## Build a REST API

### `djangorestframework`

1. Add dependency `djangorestframework` via `poetry add djangorestframework`
2. Register it in `backend/settings.py` by adding `'rest_framework'` to `INSTALLED_APPS`

### Serializer

serialization is the process of transforming rich data (objects, arrays) into a string (e.g. in `JSON` format) so it can be easily sent around.

Here we define the model to write as `JSON` and specify which fields to include -> all of them!

Create a new file `shows/serializers.py` and fill it with:

```python
from rest_framework import serializers
from .models import Show

class ShowSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Show
        fields = '__all__'
```

### Add a view to list all shows

1. Let's make `shows/views.py` be the following:

    ```python
    from rest_framework.views import APIView
    from rest_framework.response import Response 

    from .models import Show
    from .serializers import ShowSerializer

    class ShowListView(APIView):
        # `_request` is not used. The leading underscore expresses that it won't be used.
        def get(self, _request):
            shows = Show.objects.all()
            serialized_shows = ShowSerializer(shows, many=True)
            return Response(serialized_shows.data)
    ```

2. `url` path

    Make a new file called `shows/urls.py`. Add the path for the index/list view. You can copy/paste this code into `shows/urls.py`:

    ```python
    from django.urls import path
    from .views import ShowListView

    urlpatterns = [
        path('', ShowListView.as_view()),
    ]
    ```

3. In `backend/urls.py` add a new endpoint to `urlpatterns`:

    ```python
    from django.urls import path, include # <- add `include` to the import

    path('shows/', include('shows.urls')) # <- add this line
    ```

4. Test `http://localhost:8000/shows/` in the browser

5. Add `http://localhost:8000/shows/` to your **Insomnia** or **Postman** request collection and test the request there.

### Add a second view to retrieve a particular show

1. Let's add another view to `shows/views.py`:

    Add this new `ShowDetailView` class

    ```python
    class ShowDetailView(APIView):
        def get(self, _request, pk):
            show = Show.objects.get(id=pk)
            serialized_shows = ShowSerializer(show, many=False)
            return Response(serialized_shows.data)
    ```

2. Add detail `url` path to `shows/urls.py`:

    We want to establish the route `shows/<some_number>`

    ```python
    from django.urls import path
    from .views import ShowListView, ShowDetailView # <- add `ShowDetailView` here 

    urlpatterns = [
        path('', ShowListView.as_view()),
        path('<str:pk>/', ShowDetailView.as_view()) # <- add this line
    ]
    ```

3. Test `http://localhost:8000/shows/1` in your browser
4. Test `http://localhost:8000/shows/20` in your browser
5. Add `http://localhost:8000/shows/1` to your **Insomnia** or **Postman** request collection and test the request there.


## Oh no! We forgot a field in the database!

1. Add the field `number_of_seasons` to the `Show` model in `shows/models.py`:

   ```python
   number_of_seasons = models.PositiveIntegerField(default=None)
   ```

2. Create a new migration
3. Run migrations
4. Go to the admin panel and add the number of seasons for all entries.

## React Client App

### CORS

