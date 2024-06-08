#! /bin/bash

# Global variables
DIR_PATH=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
VENV_PATH="$DIR_PATH/.venv"
PYTHON3_11="$VENV_PATH/bin/python3.11"
SCRIPT_FILE="$DIR_PATH/src/data_collection/main.py"
LOG_PATH="$DIR_PATH/logs"
LOG_FILE="$LOG_PATH/data_collection.log"

# Script
mkdir -p $LOG_PATH

echo "[$(date '+%d-%m-%Y %H:%M:%S')]" > $LOG_FILE

# check if venv is not setup
if [ ! -d "$VENV_PATH" ]; then
  echo "Error: .venv directory does not exist. Please set up the virtual environment first."
  echo "Error: .venv directory does not exist. Please set up the virtual environment first." >> $LOG_FILE
  exit 1
fi

$PYTHON3_11 $SCRIPT_FILE >> $LOG_FILE
