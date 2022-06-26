# Up and Run Project

## Option 1: With Docker (Recommended)

1. `docker-compose -f local.yml build`
2. `docker-compose -f local.yml up`

### API Docs
Visit [localhost:8000/api/docs](http://localhost:8000/api/docs) to test API endpoints and see documentation. 

### Execute Management Commands

Use `docker-compose -f local.yml run --rm`. Eg;

* `docker-compose -f local.yml run --rm django python manage.py migrate`
* `docker-compose -f local.yml run --rm django python manage.py createsuperuser`

### Running Tests

To run test, command `docker-compose -f local.yml run --rm django pytest`

## Option 2: Locally

1. Install and configure PostgreSQL
2. Create a virtualenv and activate
    * `python3.9 -m venv <virtual env path>`
    * `source <virtual env path>/bin/activate`

3. Install requirements 
   * If you're on Mac, comment out `psycopg2` in `requirements/local.txt`
   * `pip install -r requirements/local.txt`
   * If you're on Mac, `pip install psycopg2-binary` 

4. Rename `.env.local.example` to `.env`. And update database credentials in .env file.
5. Set `READ_DOT_ENV_FILE = True` inside `config/settings/base.py`
6. Run migrations
   * `python manage.py migrate`
7. Run server
   * `python manage.py runserver 0.0.0.0:8000` 
