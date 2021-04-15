# Datadog with python applications integration demo
There are three apps/services:
* ServiceA (`django3`)
* ServiceB (`fastapi`)
* ServiceC (`pyramid`)

`django3` is API with `OpenAPI` frontend at (http://127.0.0.1:8081/api/docs),
where you can make GET requests to `fastapi` and `pyramid` apps. 
The deployment is made by `docker-compose` means

## Requirements
* docker with docker-compose


## Building the container
```sh
make build
```

## Apply all django migrations
```sh
make init_db
```

## Create `dd_api_key.env` in `conf` folder:
```
DD_API_KEY=<your key goes here>
```

## Create `secret.env` for Django app in `conf` folder:
```
SECRET_KEY=<your Django secret key goes here>
```

## Deploy all containers
```sh
make up
```

## Run requests for filling datadog with data
```sh
make run_demo [DEMO_ITERATIONS=<number of requests>]
```
`number of requests` - number of test iterations, default 1

## Stop the container
```sh
make down
```
