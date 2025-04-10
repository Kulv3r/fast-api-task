# fastapi-backend

## Usage
1. `docker compose up`
2. Check it at `http://localhost:8666/v1/ping`
3. Backend, JSON based web API based on OpenAPI: `http://localhost/v1/`
4. Automatic interactive documentation with Swagger UI (from the OpenAPI backend): `http://localhost/docs`

## Backend local development, additional details

Initialize first migration (project must be up with docker compose up and contain no 'version' files)
```shell
$ docker compose exec backend alembic revision --autogenerate -m "init"
```

Create new migration file
```shell
$ docker compose exec backend alembic revision --autogenerate -m "some cool comment"
```

Apply migrations
```shell
$ docker compose exec backend alembic upgrade head
```
