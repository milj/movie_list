# movie_list

A Studio Ghibli movie list

PostgreSQL uses these variables:
```
export POSTGRES_USER="..."
export POSTGRES_PASSWORD="..."
export POSTGRES_HOST="..."
export POSTGRES_PORT="..."
```

Database name in the settings: `movie_list`

Packages to install ("where does the `requirements.txt` come from?"):
```
pip install Django psycopg2 requests pytest-django pytest-describe pytest-vcr expects freezegun
```

Regarding movie list update: I assumed setting up Celery
and defining periodic task there would be an overkill for this project.
Update every minute is a hint at `cron` (1 minute is its lowest granularity),
so I wrote a `ghibli_etl_run` management command that is supposed to be run by `cron`
(to be set up on the server):

```
crontab -e
*/1 * * * * /path/to/python /path/to/manage.py ghibli_etl_run
```

Running the tests:
```
pytest
```

Things left to do in the tests:
* Mocking database calls (e.g. in the view test) to speed up the tests
* An overarching integration test script, meant to be run manually when needed
(not as part of standard test suite). The test would setup Django with a test database, run the ETL management command
(fetch data from the real API), then access the 'localhost:8000/movies/' and look for plausible strings.
* Tests of API errors handling (simulating no network, malformed JSON response etc.)
* Testing that correct messages are logged in different error/warning situations
* More strict view/template test, not just searching for strings
