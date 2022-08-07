<h1 align="center">E-menu app for managing menu cards and dishes</h1>

<center>

![FastAPI](https://img.shields.io/badge/fastapi-%23009485.svg?style=for-the-badge&logo=fastapi&logoColor=white) ![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white) ![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white) 
<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a> <a href="https://www.python.org/dev/peps/pep-0008/"><img alt="Code style: pep8" src="https://img.shields.io/badge/code%20style-pep8-orange.svg"></a>

</center>

## 1. Frameworks and libraries used
[Fastapi](https://www.djangoproject.com/)
[Uvicorn](https://www.uvicorn.org/)
[Sqlalchemy](https://www.sqlalchemy.org/)
[Alembic](https://alembic.sqlalchemy.org/)


## 2. Requirements

This development setup is tested in Linux environment. Overall components are deployed in Docker environment. It might work in Docker in Windows environment; try at your own risk.

### Below software requirements are needed for the overall setup to work.
* **Docker:** container runtime environment
* **Docker-compose:** to package and manage multiple images together
* (Optional) **Make:** to execute the makefile to help setup the development environment with minimum effort (recommended).
* (Optional) **Python version minimum 3.8:** if developing in local environment

## 3. Development instruction with Docker

1. Clone github repository and go inside repository folder.
2. Create your .env file from .env.example or add names from this file to environment variables.
3. Ensure 8000 and 5432 are not in use. If not possible, ports definitions can be changed in docker-compose.yml.
4. Build and start project with docker compose. Run with make: `make buildup` or with docker command : `docker-compose up --build` for V1 or `docker compose up --build` for V2.
5. To load initial data into database run command `make db-load` or enter postgres container and run `psql -d $(DATABASE_NAME) -U $(DATABASE_USERNAME) < /docker-entrypoint-initdb.d/dump.sql`.
6. Development server is running under localhost:8000

## 4. Use
SwaggerUI API documentation is available under http://127.0.0.1:8000/docs
Alternative ReDoc documentation is under http://127.0.0.1:8000/redoc
Openapi JSON is under http://127.0.0.1:8000/v1/openapi.json 
All GET requests are publicly available. PUT, POST and DELETE queries can be used after login, except for `create-user` POST request.
