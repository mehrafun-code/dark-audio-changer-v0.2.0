# Dark Audio Changer (English → Hindi)

Video upload karo, Hindi dub milegi. Male awaaz ki jagah male Hindi voice, female ki jagah female.

## Run (Docker)
```bash
cp .env.example .env     # ANTHROPIC_API_KEY daalo (optional)
docker compose up --build
```
Browser me kholo: http://localhost:8000

## Run (bina Docker)
Requirement: Python 3.11, ffmpeg
```bash
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Structure
```
app/
  main.py        API (FastAPI)
  pipeline.py    poori dubbing pipeline
  gender.py      male/female detection
  translate.py   Claude / Google translation
  audio_utils.py ffmpeg helpers
  config.py      settings (.env)
  static/        web UI + logo.png, favicon.png
```

## Roadmap
- v0.2: Demucs (background music rakhna), pyannote speaker diarization
- v0.3: Voice cloning (XTTS-v2), more languages
- v0.4: Mobile app
