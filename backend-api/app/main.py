from fastapi import FastAPI, Depends, HTTPException
import boto3
from sqlalchemy.orm import Session
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
from sqlalchemy import func
from . import models, database
from .config import settings

app = FastAPI()

load_dotenv()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.WEBSITE_LINK],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

s3_client = boto3.client('s3')
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")

@app.get("/api/sessions")
def read_sessions(db: Session = Depends(database.get_db)):
    return db.query(models.PracticeSession).order_by(models.PracticeSession.timestamp.desc()).all()

@app.get("/api/stats")
def get_total_stats(db: Session = Depends(database.get_db)):
    stats = db.query(
        func.count(models.PracticeSession.id),
        func.sum(models.PracticeSession.note_count)
    ).first()

    return {
        "total_sessions": stats[0] or 0,
        "total_notes": stats[1] or 0
    }
@app.get("/api/midi/{session_id}", response_model=None)
async def serve_midi(session_id: int, db: Session = Depends(database.get_db)):
    session_record = db.query(models.PracticeSession).filter(models.PracticeSession.id == session_id).first()

    if not session_record:
        raise HTTPException(status_code=404, detail="Session not found")

    s3_key = session_record.s3_key

    try:
        s3_object = s3_client.get_object(Bucket=S3_BUCKET_NAME, Key=s3_key)

        return StreamingResponse(
            s3_object['Body'],
            media_type="audio/midi",
            headers={
                "Content-Disposition": f"attachment; filename={os.path.basename(str(s3_key))}",
                "Access-Control-Expose-Headers": "Content-Disposition"
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))