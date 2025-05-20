from fastapi import FastAPI, status
from fastapi.exceptions import HTTPException
from pydantic import BaseModel
from typing import List
import uuid

app = FastAPI()

class NoteIn(BaseModel):
    name: str
    treatment: str
    duration: int
    content: str

class Note(NoteIn):
    id: str

class UpdateNote(BaseModel):
    content: str

db = {}


@app.get('/')
async def read_root():
    return {"message": "Hello world"}

@app.post('/notes')
async def create_note(note:NoteIn):
    note_id = str(uuid.uuid4())
    full_note = Note(id=note_id, **note.model_dump())
    db[note_id] = full_note
    
    return full_note

@app.get('/notes')
async def get_notes():
    return{"notes": list(db.values())}

@app.get('/notes/{note_id}')
async def get_note_by_id(note_id:str):
    if note_id in db:
        return{"id": note_id, "note": db[note_id]}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail ="Note Not Found")

@app.put('/notes/{note_id}')
async def update_note(note_id:str, note_update:UpdateNote):
    for note_id in db:
        updated_note = db[note_id].copy(update={"content": note_update.content})
        db[note_id] = updated_note
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")

@app.delete('/notes/{note_id}')
async def delete_note(note_id:str):
    if note_id in db:
            del db[note_id]
            return
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
