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

Run app

```
docker build -t order-service ./app/
docker run --name order-service --network order-network -e DATABASE_URL=postgresql://postgres:password@order-db:5432/orderdb -p 8000:8000 -d order-service
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

* Add email validation
* Unit & integration tests
* Implement an external solution (eg redis) for caching taken emails (now when multiple service instances are running, each one only keeps its own set of emails)
* Find out another way to inject db (not pass from router through all layers, although [FastApi author considers this way optimal](https://github.com/fastapi/fastapi/pull/5489#issuecomment-1312401548))
