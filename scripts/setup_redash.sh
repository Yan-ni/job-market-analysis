#! /bin/bash

# Global variables
DIR_PATH=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

DOCKER_COMPOSE_FILE="$DIR_PATH/../docker-compose.redash.yml"

docker compose -f $DOCKER_COMPOSE_FILE run --rm redash-server create_db
