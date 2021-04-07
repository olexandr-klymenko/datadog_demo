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


## Stop the container
```sh
make down
```

## How to filter log messages by trace_id
In search field put following query:
```
dd.trace_id\=<TRACE_ID>
```