# Django and TimescaleDB Test

Test integrating TimescaleDB into Django. To start and setup the database:

    docker run -d --rm --name timescaledb -p 127.0.0.1:5432:5432 -e POSTGRES_PASSWORD=password timescale/timescaledb:latest-pg12
    psql -h 127.0.0.1 -U postgres
    --> password
    --> CREATE DATABASE sensors;
    --> ctrl + D
    pipenv shell
    cd django_timescale
    ./manage.py migrate
    ./manage.py loaddata test_data.json

To start the dev server run `./manage.py runserver`

In order to test the smearing of timestamps on collisions run `curl -d "value=<float>" 127.0.0.1:8000/go/` several times while replacing <float> with a number. Then check the resulting timestamps in the terminal output or the admin view. The newely inserted value should always have a timestamp 1 microsecond greater than the last one (timestamp is hard coded into the view). 
