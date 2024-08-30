# Planetarium API service

API service for planetarium service management written on DRF

## Installing using GitHub

``` shell
git clone https://github.com/YESosnovska/planetarium-api-service.git
cd planetarium-api-service
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
set DB_HOST=<your db hostname>
set DB_NAME=<your db name>
set DB_USER=<your db username>
set DB_PASSWORD=<your db user password>
set SECRET_KEY=<your secret key>
python manage.py migrate
python manage.py runserver
```

## Run with Docker 

```shell
docker-compose build
docker-compose up
```

## Getting access

- create user via /api/user/register/
- get access token via /api/user/token/


## Features 

- JWT authenticated
- Admin panel /admin/
- Documentation is located at /api/doc/swagger/
- Managing reservations and tickets
- Creating astronomy shows with themes, description
- Creating planetarium domes
- Adding Show Sessions
- Filtering astronomy shows and show sessions
