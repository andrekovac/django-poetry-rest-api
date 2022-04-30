# Django Shell

1. Open a django shell

	```sh
	python manage.py shell
	```

2. Import your models

	```sh
	from locations.models import Location
	```

3. Get all stored instances of the model

	```sh
	Location.objects.all()
	```
	
4. Retrieve related model instances (e.g. in a many-to-many relationship)


	```sh
	Location.objects.all()[0].books_taking_place_at.all()
	```
	
	- Here the `related_name` is `books_taking_place_at`.
	- So books of a particular location can be retrieved from a location via `books_taking_place_at`

5. Exit the django shell via `exit()`

