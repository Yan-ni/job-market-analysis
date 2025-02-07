#! /bin/bash

# Variables
DIR_PATH=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
DA_MAIN_SCRIPT_FILE="$DIR_PATH/data_collection.sh --container da-script"
DS_MAIN_SCRIPT_FILE="$DIR_PATH/data_collection.sh --container ds-script"
UPDATE_DELETED_SCRIPT_FILE="$DIR_PATH/update_deleted.sh"
CLEAN_DATA_SCRIPT_FILE="$DIR_PATH/clean_data.sh"
TEMP_CRON="/tmp/crontab_temp"

# Script
crontab -l > "$TEMP_CRON"

echo "0 0 * * * $CLEAN_DATA_SCRIPT_FILE" >> "$TEMP_CRON" # Every day at midnight

echo "0 1 * * * $DA_MAIN_SCRIPT_FILE" >> "$TEMP_CRON" # Every day at 01:00

echo "0 3 * * * $DS_MAIN_SCRIPT_FILE" >> "$TEMP_CRON" # Every day at 03:00

echo "0 5 * * * $UPDATE_DELETED_SCRIPT_FILE" >> "$TEMP_CRON" # Every day at 05:00


crontab "$TEMP_CRON"

rm "$TEMP_CRON"

service cron reload
