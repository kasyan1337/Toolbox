#!/bin/bash

export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init --path)"
eval "$(pyenv init -)"

cd /Users/kasimjanci/PycharmProjects/Toolbox/whisper_dictation
PYTHON=$(pyenv which python)

APP_PATH="/Users/kasimjanci/PycharmProjects/Toolbox/whisper_dictation/whisper_dictation.py"
PID=$(pgrep -f "$APP_PATH")

if [ -z "$PID" ]; then
    osascript -e 'display notification "Starting Whisper Dictation..." with title "Whisper"'
    "$PYTHON" "$APP_PATH"
else
    osascript -e 'display notification "Stopping Whisper Dictation..." with title "Whisper"'
    kill "$PID"
fi