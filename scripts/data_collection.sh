#! /bin/bash

# Global variables
DIR_PATH=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

DOCKER_COMPOSE_FILE="$DIR_PATH/../docker-compose.yml"

CONTAINER_NAME=$2

docker compose -f $DOCKER_COMPOSE_FILE up -d db $CONTAINER_NAME
