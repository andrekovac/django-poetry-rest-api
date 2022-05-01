# Django Shell

1. Open a django shell

	```sh
	python manage.py shell
	```

2. Import your models

	```python
	from locations.models import Location
	```

3. Get all stored instances of the model

	```python
	Location.objects.all()
	```
	
4. Retrieve related model instances (e.g. in a many-to-many relationship)


	```python
	Location.objects.all()[0].books_taking_place_at.all()
	```
	
	- Here the `related_name` is `books_taking_place_at`.
	- So books of a particular location can be retrieved from a location via `books_taking_place_at`

	**Alternative**:

	```python
	Location.objects.all().get(id=1).books_taking_place_at.all()
	```

5. Exit the django shell via `exit()`


## More queries

See the entire documentation about [Django queries](https://docs.djangoproject.com/en/4.0/topics/db/queries/).

### Examples

**Example**: Get all books who's title begins with "What"

```python
q = Book.objects.filter(title__startswith="What")
```
