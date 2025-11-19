import os
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime, timezone

from database import db, create_document, get_documents
from schemas import HealingSession, JournalEntry

app = FastAPI(title="Sound Healing API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Sound Healing API is running"}

@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }

    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Configured"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"

    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"

    return response

# --------- Models for API requests ---------
class ToneRequest(BaseModel):
    frequency: float
    duration: int  # seconds
    waveform: str = "sine"  # sine, square, triangle

class SessionLogRequest(HealingSession):
    pass

class JournalRequest(JournalEntry):
    pass

# --------- API Endpoints ---------

@app.get("/api/tracks")
def list_tracks():
    """Static curated list of relaxing tracks (tones and nature)."""
    tracks = [
        {"id": "tone-432", "name": "432 Hz Pure Tone", "type": "tone", "frequency": 432},
        {"id": "tone-528", "name": "528 Hz Love Frequency", "type": "tone", "frequency": 528},
        {"id": "tone-963", "name": "963 Hz Crown", "type": "tone", "frequency": 963},
        {"id": "nature-rain", "name": "Gentle Rain", "type": "nature"},
        {"id": "nature-forest", "name": "Forest Ambience", "type": "nature"},
        {"id": "bowl-c4", "name": "Crystal Bowl C4", "type": "bowl", "note": "C4"},
    ]
    return {"tracks": tracks}

@app.post("/api/sessions")
def log_session(payload: SessionLogRequest):
    try:
        inserted_id = create_document("healingsession", payload)
        return {"ok": True, "id": inserted_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/sessions")
def get_recent_sessions(limit: int = 20):
    try:
        docs = get_documents("healingsession", {}, limit)
        # Cast ObjectId and dates to serializable
        def serialize(doc):
            doc["id"] = str(doc.pop("_id", ""))
            for k in ["created_at", "updated_at"]:
                if k in doc and hasattr(doc[k], "isoformat"):
                    doc[k] = doc[k].isoformat()
            return doc
        return {"sessions": [serialize(d) for d in docs[::-1]]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/journal")
def create_journal(payload: JournalRequest):
    try:
        inserted_id = create_document("journalentry", payload)
        return {"ok": True, "id": inserted_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/journal")
def list_journal(limit: int = 50):
    try:
        docs = get_documents("journalentry", {}, limit)
        def serialize(doc):
            doc["id"] = str(doc.pop("_id", ""))
            for k in ["created_at", "updated_at"]:
                if k in doc and hasattr(doc[k], "isoformat"):
                    doc[k] = doc[k].isoformat()
            return doc
        return {"entries": [serialize(d) for d in docs[::-1]]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
