# Datadog with python applications integration demo

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

## Deploy all containers
```sh
make up
```

## Run requests for filling datadog with data
```sh
make DEMO_ITERATIONS=<number of requests> run_demo
```
`number of requests` - number of requests to fill datadog with data, default 100

## Stop the container
```sh
make down
```

## How to filter log messages by trace_id
In search field put following query:
```
dd.trace_id\=<TRACE_ID>
```