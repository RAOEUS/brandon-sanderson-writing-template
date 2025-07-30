#!/bin/bash
set -e

# 1. Create virtual environment
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
fi

# 2. Activate venv
source .venv/bin/activate

# 3. Install dependencies
echo "Installing requirements..."
pip install --upgrade pip
pip install -r requirements.txt

# 4. Optional HTML title/h1 customization
HTML_FILE="editor/index.html"
DEFAULT_TEXT="Sanderson Novel Template Editor"

if grep -q "$DEFAULT_TEXT" "$HTML_FILE"; then
    echo "Detected default title and heading: \"$DEFAULT_TEXT\""

    read -p "Enter a custom title for the browser tab (press Enter to skip): " TITLE_INPUT
    if [ -n "$TITLE_INPUT" ]; then
        sed -i "s|<title>.*</title>|<title>$TITLE_INPUT</title>|" "$HTML_FILE"
        echo "✅ Replaced <title> with: $TITLE_INPUT"
    else
        echo "⏩ Skipped <title> replacement."
    fi

    read -p "Enter a custom heading (h1) for the page (press Enter to skip): " HEADING_INPUT
    if [ -n "$HEADING_INPUT" ]; then
        sed -i "s|<h1 class=\"text-3xl.*\">.*</h1>|<h1 class=\"text-3xl font-bold mb-4\">$HEADING_INPUT</h1>|" "$HTML_FILE"
        echo "✅ Replaced <h1> with: $HEADING_INPUT"
    else
        echo "⏩ Skipped <h1> replacement."
    fi

    read -p "Enter your name to display under the heading (press Enter to skip): " AUTHOR_NAME
    if [ -n "$AUTHOR_NAME" ]; then
        # Insert <h2> line after the <h1> line
        sed -i "/<h1 class=\"text-3xl.*\">.*<\/h1>/a <h2 class=\"text-xl text-gray-600 mb-6\">by $AUTHOR_NAME</h2>" "$HTML_FILE"
        echo "✅ Inserted <h2> author name: $AUTHOR_NAME"
    else
        echo "⏩ Skipped <h2> author line."
    fi
else
    echo "⏩ HTML already customized, skipping prompts."
fi

# 5. Start the FastAPI app
echo "🚀 Starting server..."
nohup python3 -m uvicorn app:app --reload --host 127.0.0.1 --port 8000 > server.log 2>&1 &

# 6. Open browser
sleep 2
xdg-open http://127.0.0.1:8000 2>/dev/null || open http://127.0.0.1:8000 2>/dev/null || echo "Open your browser and go to http://127.0.0.1:8000"

echo "✅ Editor running at http://127.0.0.1:8000"

