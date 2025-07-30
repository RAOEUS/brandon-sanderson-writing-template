from fastapi import FastAPI, Request, Body
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from pathlib import Path
from git import Repo
from typing import List
import os

app = FastAPI()

BASE_DIR = Path(__file__).parent
MD_DIR = BASE_DIR / "markdown"
HTML_DIR = BASE_DIR / "editor"
REPO = Repo(BASE_DIR)

class FileUpdate(BaseModel):
    content: str

@app.get("/files")
def list_files():
    return sorted([f.name for f in MD_DIR.glob("*.md")])

@app.get("/files/{filename}")
def get_file(filename: str):
    file_path = MD_DIR / filename
    if file_path.exists():
        return FileResponse(file_path)
    return JSONResponse(status_code=404, content={"error": "File not found"})

@app.put("/files/{filename}")
def save_file(filename: str, data: FileUpdate):
    file_path = MD_DIR / filename
    file_path.write_text(data.content, encoding="utf-8")
    return {"status": "ok"}

# --- Git API Endpoints ---

@app.get("/git/status")
def git_status():
    changed = [item.a_path for item in REPO.index.diff(None)]
    untracked = REPO.untracked_files
    return {"changed": changed, "untracked": untracked}

@app.post("/git/commit")
def git_commit(message: str = Body(...)):
    REPO.git.add(all=True)
    REPO.index.commit(message)
    return {"status": "committed", "message": message}

@app.post("/git/push")
def git_push():
    origin = REPO.remote(name="origin")
    origin.push()
    return {"status": "pushed"}

@app.post("/git/pull")
def git_pull():
    origin = REPO.remote(name="origin")
    origin.pull()
    return {"status": "pulled"}

@app.get("/git/log")
def git_log():
    return [{"message": c.message.strip(), "hexsha": c.hexsha[:7]} for c in REPO.iter_commits('main', max_count=10)]

# Mount frontend
app.mount("/", StaticFiles(directory=HTML_DIR, html=True), name="static")
