# Techstaff Inventory

## Project Team: OJBK

## Team Member

- Weikai Liang (Prooduct Manager)
- Yuan Chen, Jun Chen, Kai Lynn

## Guidance
- Before running the server, install the requirements:
    In the project directory, type in ```pip install -r requirements.txt``` in terminal.
    
- Run server by:
    In the project directory, type in ```python manage.py runserver``` in terminal.
    
- Create an admin account:
    In the project directory, type in ```python manage.py createsuperuser``` in terminal.

## Dockerfile
```
FROM python:3.8
ENV PYTHONUNBUFFERED 1
WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
COPY . /app
```
## docker-compose.yml

```
version: '3'
services:
  db:
    image: mysql:8
    ports:
      - "3306:3306"
    environment:
      - MYSQL_DATABASE='mydatabase'
      - MYSQL_USER='root'
      - MYSQL_PASSWORD='some_password'
      - MYSQL_ROOT_PASSWORD='some_password'
      - MYSQL_HOST=''
    volumes:
      - /tmp/app/mysqld:/var/run/mysqld
      - ./db:/var/lib/mysql
  web:
    build: .
    command: python manage.py runserver 0.0.0.0:8000
    ports:
      - "8000:8000"
    volumes:
      - .:/app
      - /tmp/app/mysqld:/run/mysqld
    depends_on:
      - db
```