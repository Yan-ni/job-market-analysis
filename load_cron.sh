#! /bin/bash

# Variables
DIR_PATH=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
SCRIPT_FILE="$DIR_PATH/data_collection.sh"
TEMP_CRON="/tmp/crontab_temp"

# Script
crontab -l > "$TEMP_CRON"

echo "0 3 * * * $SCRIPT_FILE" >> "$TEMP_CRON" # Every day at 03:00

crontab "$TEMP_CRON"

rm "$TEMP_CRON"
