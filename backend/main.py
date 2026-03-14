import whisper
import tempfile
import os
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow React frontend to talk to this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the Whisper model (using "base" for speed, can change later)
model = whisper.load_model("base")

@app.get("/")
def read_root():
    return {"message": "Transcription API is running!"}

@app.post("/transcribe")
async def transcribe(file: UploadFile = File(...)):
    # Save uploaded file to a temp location
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as tmp:
        contents = await file.read()
        tmp.write(contents)
        tmp_path = tmp.name

    # Run Whisper transcription
    result = model.transcribe(tmp_path)

    # Clean up the temp file
    os.remove(tmp_path)

    return {
        "text": result["text"],
        "segments": result["segments"]
    }