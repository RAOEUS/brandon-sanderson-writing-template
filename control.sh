#!/bin/bash

APP_NAME="app"
PID_FILE=".server.pid"
HOST="127.0.0.1"
PORT="8000"

function start_server() {
    if [ -f "$PID_FILE" ] && kill -0 $(cat "$PID_FILE") 2>/dev/null; then
        echo "⚠️ Server is already running (PID $(cat "$PID_FILE"))"
        exit 1
    fi

    echo "🚀 Starting $APP_NAME..."
    uvicorn $APP_NAME:app --host $HOST --port $PORT &

    echo $! > "$PID_FILE"
    echo "✅ Server started with PID $(cat "$PID_FILE")"
}

function stop_server() {
    if [ ! -f "$PID_FILE" ]; then
        echo "❌ No PID file found. Is the server running?"
        exit 1
    fi

    PID=$(cat "$PID_FILE")
    if kill -0 "$PID" 2>/dev/null; then
        echo "🛑 Stopping server (PID $PID)..."
        kill "$PID"
        rm "$PID_FILE"
        echo "✅ Server stopped."
    else
        echo "⚠️ No running process with PID $PID. Cleaning up."
        rm "$PID_FILE"
    fi
}

function restart_server() {
    stop_server
    start_server
}

case "$1" in
    --start) start_server ;;
    --stop) stop_server ;;
    --restart) restart_server ;;
    *)
        echo "Usage: $0 [--start|--stop|--restart]"
        exit 1
        ;;
esac

