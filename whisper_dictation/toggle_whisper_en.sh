#!/bin/bash
# toggle_whisper_en.sh – logs included

# Function to output a timestamped log message
log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1"
}

# Define fixed Python interpreter and application path
PYTHON="/Library/Frameworks/Python.framework/Versions/3.12/bin/python3"
APP_PATH="/Users/kasimjanci/PycharmProjects/Toolbox/whisper_dictation/whisper_dictation_en.py"

log "Script started with argument: $1"
log "Using PYTHON: ${PYTHON}"
log "Using APP_PATH: ${APP_PATH}"

# Find running instance(s) of the script
PIDS=$(pgrep -f "$APP_PATH")
log "Current PIDs: ${PIDS}"

if [ "$1" = "start" ]; then
    if [ -z "$PIDS" ]; then
        log "No running instance found. Starting Whisper Dictation."
        # Using nohup to run in background; output is echoed for logging.
        nohup "$PYTHON" "$APP_PATH" > /dev/null 2>&1 &
        log "Started process with nohup."
        osascript -e 'display notification "Starting Whisper Dictation..." with title "Whisper"'
    else
        log "Whisper Dictation is already running."
        osascript -e 'display notification "Whisper Dictation already running" with title "Whisper"'
    fi
elif [ "$1" = "stop" ]; then
    if [ -n "$PIDS" ]; then
        log "Found running instance(s) ($PIDS). Stopping Whisper Dictation."
        # Send SIGINT to trigger the graceful shutdown in the Python process.
        echo "$PIDS" | xargs kill -SIGINT
        log "Sent SIGINT to PIDs."
        osascript -e 'display notification "Stopping Whisper Dictation..." with title "Whisper"'
    else
        log "No running instance found to stop."
        osascript -e 'display notification "Whisper Dictation is not running" with title "Whisper"'
    fi
else
    log "No valid argument provided. Use 'start' or 'stop'."
    osascript -e 'display notification "Invalid argument for toggle_whisper_en.sh" with title "Whisper"'
    exit 1
fi

log "Script finished."