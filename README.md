# Django and TimescaleDB Test

Test integrating TimescaleDB into Django. It requires a [PostgreSQL](https://www.postgresql.org/download/) client and [Pipenv](https://pipenv-fork.readthedocs.io/en/latest/install.html) to be installed. To start and setup the database.

    docker run -d --rm --name timescaledb -p 127.0.0.1:5432:5432 -e POSTGRES_PASSWORD=password timescale/timescaledb:latest-pg12
    psql -h 127.0.0.1 -U postgres
    --> password
    --> CREATE DATABASE sensors;
    --> \q
    pipenv install
    pipenv shell
    ./manage.py migrate
    ./manage.py loaddata test_data.json

To start the dev server run `./manage.py runserver`

In order to test the smearing of timestamps on collisions, in another terminal, run `curl -d "value=<float>" 127.0.0.1:8000/go/` several times while replacing `<float>` with a number. Then check the resulting timestamps in the terminal output or the admin view. The newely inserted value should always have a timestamp 1 microsecond greater than the last one (timestamp is hard coded into the view).

## Troubleshooting

### Wrong Python Version

If you only have Python 3.7 installed, change the definition in Pipfile from `python_version = "3.8"` to `python_version = "3.7"`

### Python manage.py not executing

On Windows run `py manage.py` to execute the `manage.py` commands.

### Error on migration with compress_segmentby command

If the following error is thrown during a migration, check and update the column name:  `django.db.utils.ProgrammingError: column "peripheral_component" specified in option timescaledb.compress_segmentby does not exist`. Connect to the database server with the above `psql` command, connect to the database with `\c <database_name>`, list the tables with `\dt` and show the table schema of the table to be converterd to a hypertable with `\d <table_name>`. Sometimes foreign keys have `_id` appended to their column name. In this example the variables are

- database_name: sensors
- table_name: farms_sensorreading