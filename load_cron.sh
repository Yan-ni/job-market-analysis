#! /bin/bash

# Variables
DIR_PATH=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
MAIN_SCRIPT_FILE="$DIR_PATH/data_collection.sh"
UPDATE_DELETED_SCRIPT_FILE="$DIR_PATH/update_deleted.sh"
TEMP_CRON="/tmp/crontab_temp"

# Script
crontab -l > "$TEMP_CRON"

echo "0 3 * * * $MAIN_SCRIPT_FILE" >> "$TEMP_CRON" # Every day at 03:00

echo "0 5 * * * $UPDATE_DELETED_SCRIPT_FILE" >> "$TEMP_CRON" # Every day at 05:00

crontab "$TEMP_CRON"

rm "$TEMP_CRON"

service cron reload
