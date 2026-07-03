import asyncio
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import subprocess
import os
import json
import re

ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class BuildRequest(BaseModel):
    requirements: str

@app.post("/api/build")
async def build_app(req: BuildRequest):
    async def log_generator():
        # Spawn the crew in a subprocess and capture stdout
        process = await asyncio.create_subprocess_exec(
            "uv", "run", "python", "backend/run_crew_cli.py", req.requirements,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.STDOUT
        )
        
        skip_requirements = False
        while True:
            line_bytes = await process.stdout.readline()
            if not line_bytes:
                break
            raw_line = line_bytes.decode("utf-8")
            line = ansi_escape.sub('', raw_line)

            if "--requirements" in line:
                continue
            if "│  Task:" in line:
                yield json.dumps({"log": "│  Task: [Task description omitted for brevity]                │"}) + "\n"
                skip_requirements = True
                continue
            
            if skip_requirements:
                # If we hit an empty box line or the bottom of the box, stop skipping
                if "╰─" in line or line.strip() == "│                                                                              │":
                    skip_requirements = False
                    if "╰─" in line:
                        yield json.dumps({"log": line.strip()}) + "\n"
                continue
            
            if len(line) > 200:
                yield json.dumps({"log": line[:200].strip() + "... [truncated]"}) + "\n"
            else:
                yield json.dumps({"log": line.strip()}) + "\n"
            
        await process.wait()
        yield json.dumps({"status": "completed"}) + "\n"

    return StreamingResponse(log_generator(), media_type="application/x-ndjson")

@app.get("/api/code")
async def get_code():
    sandbox_dir = "sandbox"
    
    design_code = ""
    design_path = os.path.join(sandbox_dir, "design.md")
    if os.path.exists(design_path):
        with open(design_path, "r") as f:
            design_code = f.read()

    files = []
    if os.path.exists(sandbox_dir):
        for root, dirs, filenames in os.walk(sandbox_dir):
            if ".venv" in root or "__pycache__" in root:
                continue
            for filename in filenames:
                if filename == ".DS_Store" or filename == "design.md":
                    continue
                file_path = os.path.join(root, filename)
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()
                except UnicodeDecodeError:
                    content = "[Binary File]"
                
                rel_path = os.path.relpath(file_path, sandbox_dir)
                files.append({
                    "path": rel_path,
                    "content": content
                })
                
    files.sort(key=lambda x: x["path"])
            
    return {
        "design_code": design_code,
        "files": files
    }

@app.post("/api/run-sandbox")
async def run_sandbox():
    sandbox_dir = "sandbox"
    app_path = os.path.join(sandbox_dir, "app.py")
    if not os.path.exists(app_path):
        return {"status": "error", "message": "app.py not found"}
        
    env = os.environ.copy()
    env["GRADIO_SERVER_PORT"] = "7861"
    env["GRADIO_SERVER_NAME"] = "127.0.0.1"
    
    # Kill any existing process on 7861
    try:
        subprocess.run("lsof -t -i:7861 | xargs kill -9", shell=True, check=False, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
    except Exception:
        pass
        
    # Run detached without inheriting file descriptors to prevent request hangs
    log_file = open(os.path.join(sandbox_dir, "sandbox.log"), "w")
    subprocess.Popen(
        ["uv", "run", "app.py"],
        cwd=sandbox_dir,
        env=env,
        stdout=log_file,
        stderr=subprocess.STDOUT,
        close_fds=True
    )
    
    return {"status": "started", "port": 7861}

from fastapi.responses import Response
import io
import zipfile

@app.get("/api/download")
async def download_codebase():
    sandbox_dir = "sandbox"
    download_filename = "generated_app.zip"
    
    # Try to extract a smart name from design.md
    design_path = os.path.join(sandbox_dir, "design.md")
    if os.path.exists(design_path):
        try:
            with open(design_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line.startswith("# "):
                        title = line[2:].strip()
                        # Slugify the title and remove '-design' if present at the end
                        slug = re.sub(r'[^a-zA-Z0-9]+', '-', title).strip('-').lower()
                        slug = re.sub(r'-design$', '', slug)
                        if slug:
                            download_filename = f"{slug}.zip"
                        break
        except Exception:
            pass
            
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
        
        # Add all files from sandbox
        if os.path.exists(sandbox_dir):
            for root, dirs, files in os.walk(sandbox_dir):
                if ".venv" in root:
                    continue
                for file in files:
                    if file == ".DS_Store":
                        continue
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, sandbox_dir)
                    zip_file.write(file_path, arcname)
                    
    return Response(
        content=zip_buffer.getvalue(),
        media_type="application/zip",
        headers={"Content-Disposition": f"attachment; filename={download_filename}"}
    )
