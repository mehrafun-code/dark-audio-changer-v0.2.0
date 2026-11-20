import shutil
import uuid
from pathlib import Path

from fastapi import BackgroundTasks, FastAPI, File, HTTPException, UploadFile
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from . import config
from .pipeline import process

app = FastAPI(title="Dark Audio Changer", version=config.VERSION)
JOBS: dict[str, dict] = {}
STATIC = Path(__file__).parent / "static"


def _work(job_id: str, video: Path):
    def progress(msg, pct):
        JOBS[job_id].update(status="processing", message=msg, progress=pct)
    try:
        out, segs = process(video, config.DATA_DIR / job_id, progress)
        JOBS[job_id].update(status="done", output=str(out), segments=segs, progress=100)
    except Exception as e:
        JOBS[job_id].update(status="error", message=str(e))


@app.get("/api/version")
def version():
    return {"version": config.VERSION}


@app.post("/api/dub")
async def dub(bg: BackgroundTasks, file: UploadFile = File(...)):
    job_id = uuid.uuid4().hex[:12]
    folder = config.DATA_DIR / job_id
    folder.mkdir(parents=True, exist_ok=True)
    video = folder / ("input" + Path(file.filename or "v.mp4").suffix)
    with open(video, "wb") as f:
        shutil.copyfileobj(file.file, f)
    JOBS[job_id] = {"status": "queued", "message": "Queue me hai", "progress": 0}
    bg.add_task(_work, job_id, video)
    return {"job_id": job_id}


@app.get("/api/status/{job_id}")
def status(job_id: str):
    j = JOBS.get(job_id)
    if not j:
        raise HTTPException(404, "Job nahi mila")
    return {k: v for k, v in j.items() if k != "output"}


@app.get("/api/download/{job_id}")
def download(job_id: str):
    j = JOBS.get(job_id)
    if not j or j.get("status") != "done":
        raise HTTPException(404, "Abhi ready nahi")
    return FileResponse(j["output"], media_type="video/mp4", filename="dark_audio_changer_hindi.mp4")


app.mount("/", StaticFiles(directory=STATIC, html=True), name="static")
