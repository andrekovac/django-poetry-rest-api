# Database seeding

## Create seed data

1. Replace `books` with your desired app name!

```sh
python manage.py dumpdata books --output books/seeds.json --indent=2
```

2. You can now amend `books/seeds.json`. But make sure you use the correct data types and don't remove required fields!


## Delete all data + import seed data

Delete all database entries in **ALL** tables:

```sh
python manage.py flush
```

**Attention**: This will delete all entries from your DBs (will not delete tables). So it also deletes all users (including the admin)

Import the seed data via:

```sh
python manage.py loaddata books/seeds.json
```

You have to create the admin again:

```sh
python manage.py createsuperuser
```

