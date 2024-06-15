#! /bin/bash

# Global variables
DIR_PATH=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

DOCKER_COMPOSE_FILE="$DIR_PATH/src/data_collection/docker-compose.yml"

docker compose up -d $DOCKER_COMPOSE_FILE
