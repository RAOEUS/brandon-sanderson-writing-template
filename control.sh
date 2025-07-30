#!/bin/bash
set -e

APP_NAME="app"
PID_FILE=".server.pid"
HOST="127.0.0.1"
PORT="8000"
LOG_FILE="server.log"

function start_server() {
    if [ -f "$PID_FILE" ] && kill -0 $(cat "$PID_FILE") 2>/dev/null; then
        echo "⚠️ Server is already running (PID $(cat "$PID_FILE"))"
        exit 1
    fi

    echo "🚀 Starting $APP_NAME..."
    # Start Uvicorn with reload, logging to file, in background
    nohup python3 -m uvicorn ${APP_NAME}:app --reload --host ${HOST} --port ${PORT} > "$LOG_FILE" 2>&1 &

    echo $! > "$PID_FILE"
    echo "✅ Server started with PID $(cat "$PID_FILE")"
}

function stop_server() {
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        if kill -0 "$PID" 2>/dev/null; then
            echo "🛑 Stopping server (PID $PID)..."
            kill "$PID"
            rm "$PID_FILE"
            echo "✅ Server stopped."
            return
        else
            echo "⚠️ No running process with PID $PID. Removing stale PID file."
            rm "$PID_FILE"
        fi
    fi
    # Fallback: kill by command-line match
    if pkill -f "uvicorn ${APP_NAME}:app"; then
        echo "✅ Server killed by process name."
    else
        echo "❌ No server process found."
    fi
}

function restart_server() {
    stop_server
    start_server
}

case "$1" in
    --start)
        start_server
        ;;
    --stop)
        stop_server
        ;;
    --restart)
        restart_server
        ;;
    *)
        echo "Usage: $0 [--start|--stop|--restart]"
        exit 1
        ;;
 esac

