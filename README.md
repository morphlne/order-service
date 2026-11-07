# Order service

### How to run

#### Docker compose

```
docker-compose up --build
```

#### Docker

Create network

```
docker network create order-network
```

Run db

```
docker build -t order-db ./db/
docker run --name order-db --network order-network -e POSTGRES_PASSWORD=password -p 5432:5432 -d order-db
```

Run redis

```
docker build -t order-redis ./redis/
docker run --name order-redis --network order-network -p 6379:6379 -d order-redis
```

Run app

```
docker build -t order-service ./app/
docker run -d \
  --name order-service \
  --network order-network \
  -p 8000:8000 \
  -e DATABASE_URL="postgresql://postgres:password@order-db:5432/orderdb" \
  -e REDIS_URL="redis://redis:password@order-redis:6379/0" \
  order-service
```

#### Run app from source

PostgreSQL must be running locally

```
cd app
pip install -r requirements.txt
uvicorn main:app --reload
```

### Swagger UI

Swagger UI is accessible on http://localhost:8000/docs and OpenAPI spec on http://localhost:8000/openapi.json

### What's next

* Add Unit tests for /orders
* Add Integration tests
* Find out another way to inject db (not pass from router through all layers, although [FastApi author considers this way optimal](https://github.com/fastapi/fastapi/pull/5489#issuecomment-1312401548))
* Configure the DB container to be marked "ready" only after the DDL script has been applied
