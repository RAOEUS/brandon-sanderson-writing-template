from fastapi import FastAPI, Request, Body, Query
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from pathlib import Path
from git import Repo
from typing import List
import os
import logging

app = FastAPI()

BASE_DIR = Path(__file__).parent
PLAN_DIR = BASE_DIR / "plan"
CHAPTERS_DIR = BASE_DIR / "chapters"
HTML_DIR = BASE_DIR / "editor"
REPO = Repo(BASE_DIR)

# Setup logging
LOG_FILE = BASE_DIR / "server.log"
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.WARNING,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)

class FileUpdate(BaseModel):
    content: str

@app.get("/files")
def list_files():
    try:
        return {
            "plan": sorted([f.name for f in PLAN_DIR.glob("*.md")]),
            "chapters": sorted([f.name for f in CHAPTERS_DIR.glob("*.md")])
        }
    except Exception as e:
        logger.error(f"Error listing files: {e}")
        return JSONResponse(status_code=500, content={"error": "Internal Server Error"})

@app.get("/files/{section}/{filename}")
def get_file(section: str, filename: str):
    try:
        dir_path = PLAN_DIR if section == "plan" else CHAPTERS_DIR
        file_path = dir_path / filename
        if file_path.exists():
            return FileResponse(file_path)
        return JSONResponse(status_code=404, content={"error": "File not found"})
    except Exception as e:
        logger.error(f"Error retrieving file {filename}: {e}")
        return JSONResponse(status_code=500, content={"error": "Internal Server Error"})

@app.put("/files/{section}/{filename}")
def save_file(section: str, filename: str, data: FileUpdate):
    try:
        dir_path = PLAN_DIR if section == "plan" else CHAPTERS_DIR
        file_path = dir_path / filename
        file_path.write_text(data.content, encoding="utf-8")
        return {"status": "ok"}
    except Exception as e:
        logger.error(f"Error saving file {filename}: {e}")
        return JSONResponse(status_code=500, content={"error": "Internal Server Error"})

@app.post("/files/{section}/{filename}")
def create_file(section: str, filename: str):
    try:
        dir_path = PLAN_DIR if section == "plan" else CHAPTERS_DIR
        dir_path.mkdir(parents=True, exist_ok=True)
        file_path = dir_path / filename
        if file_path.exists():
            logger.warning(f"Tried to create existing file: {file_path}")
            return JSONResponse(status_code=400, content={"error": "File already exists"})
        file_path.write_text("", encoding="utf-8")
        return {"status": "created"}
    except Exception as e:
        logger.error(f"Error creating file {filename} in {section}: {e}")
        return JSONResponse(status_code=500, content={"error": "Internal Server Error"})

@app.delete("/files/{section}/{filename}")
def delete_file(section: str, filename: str):
    try:
        dir_path = PLAN_DIR if section == "plan" else CHAPTERS_DIR
        file_path = dir_path / filename
        if file_path.exists():
            file_path.unlink()
            return {"status": "deleted"}
        return JSONResponse(status_code=404, content={"error": "File not found"})
    except Exception as e:
        logger.error(f"Error deleting file {filename}: {e}")
        return JSONResponse(status_code=500, content={"error": "Internal Server Error"})

@app.get("/git/status")
def git_status():
    try:
        changed = [item.a_path for item in REPO.index.diff(None)]
        untracked = REPO.untracked_files
        return {"changed": changed, "untracked": untracked}
    except Exception as e:
        logger.error(f"Git status error: {e}")
        return JSONResponse(status_code=500, content={"error": "Internal Server Error"})

@app.post("/git/commit")
def git_commit(message: str = Body(...)):
    try:
        REPO.git.add(all=True)
        REPO.index.commit(message)
        return {"status": "committed", "message": message}
    except Exception as e:
        logger.error(f"Git commit error: {e}")
        return JSONResponse(status_code=500, content={"error": "Internal Server Error"})

@app.post("/git/push")
def git_push():
    try:
        origin = REPO.remote(name="origin")
        origin.push()
        return {"status": "pushed"}
    except Exception as e:
        logger.error(f"Git push error: {e}")
        return JSONResponse(status_code=500, content={"error": "Internal Server Error"})

@app.post("/git/pull")
def git_pull():
    try:
        origin = REPO.remote(name="origin")
        origin.pull()
        return {"status": "pulled"}
    except Exception as e:
        logger.error(f"Git pull error: {e}")
        return JSONResponse(status_code=500, content={"error": "Internal Server Error"})

@app.get("/git/log")
def git_log():
    try:
        return [{"message": c.message.strip(), "hexsha": c.hexsha[:7]} for c in REPO.iter_commits('main', max_count=10)]
    except Exception as e:
        logger.error(f"Git log error: {e}")
        return JSONResponse(status_code=500, content={"error": "Internal Server Error"})

@app.get("/git/diff")
def git_diff():
    try:
        diff_output = REPO.git.diff()
        return {"diff": diff_output}
    except Exception as e:
        logger.error(f"Git diff error: {e}")
        return JSONResponse(status_code=500, content={"error": "Internal Server Error"})

@app.post("/git/add")
def git_add(filename: str = Query(...)):
    try:
        REPO.git.add(filename)
        return {"status": "added", "file": filename}
    except Exception as e:
        logger.error(f"Git add error for file {filename}: {e}")
        return JSONResponse(status_code=500, content={"error": "Internal Server Error"})

@app.post("/git/reset")
def git_reset(filename: str = Query(...)):
    try:
        REPO.git.reset(filename)
        return {"status": "unstaged", "file": filename}
    except Exception as e:
        logger.error(f"Git reset error for file {filename}: {e}")
        return JSONResponse(status_code=500, content={"error": "Internal Server Error"})

app.mount("/", StaticFiles(directory=HTML_DIR, html=True), name="static")

