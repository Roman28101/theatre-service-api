# cinema-service-api

Project of "Theatre service API". For online managing plays and performances in current theater and reserve tickets. Written on Django REST Framework


## Installing

Use this commands for installation of this project on your localhost

* Install PostgreSQL and create a data base
```shell
git clone https://github.com/Roman28101/cinema-service-api
cd theatre_service
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
* create .env file in main directory
* set data into it (use .env.sample for reference)
```shell
POSTGRES_HOST=POSTGRES_HOST
POSTGRES_DB=POSTGRES_DB
POSTGRES_USER=POSTGRES_USER
POSTGRES_PASSWORD=POSTGRES_PASSWORD
DJANGO_SECRET_KEY=DJANGO_SECRET_KEY
```
```
python manage.py migrate
python manage.py runserver
```

## Run project with docker

* Download and install [Docker](https://www.docker.com/products/docker-desktop/)
* Run in terminal:

```shell
docker-compose build
docker-compose up
```


## Get access to project

* Download [ModHeader](https://chrome.google.com/webstore/detail/modheader/idgpnmonknjnojddfkpgkljpfnnfcklj?hl=en)
* create user - /api/user/register
* get access token /api/user/token/



## Features

* JSON Web Token authenticated
* Documentation /api/doc/swagger/
* Creating plays with genres and actors
* Creating theatre halls
* Managing play tickets and reserve them
* Filtering plays by date, title
* Filtering performances by title, actors, genres
* Adding performances



## For testing features

You can use this data for testing all the features.
* for .env file: 
```shell
POSTGRES_HOST=db
POSTGRES_DB=app
POSTGRES_USER=postgres
POSTGRES_PASSWORD=supersecretpassword
DJANGO_SECRET_KEY=64&eflb&0xj977%e((z1!5q141^v3@x=sr(v-8bq2e$@y^09x9
```
