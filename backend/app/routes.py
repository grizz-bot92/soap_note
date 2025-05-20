from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from typing import List
import uuid
from app.schemas import db, Note, NoteIn, UpdateNote


note_router = APIRouter()

@note_router.get('/')
async def read_root():
    return {"message": "Hello world"}

@note_router.post('/notes')
async def create_note(note:NoteIn):
    note_id = str(uuid.uuid4())
    full_note = Note(id=note_id, **note.model_dump())
    db[note_id] = full_note
    
    return full_note

@note_router.get('/notes')
async def get_notes():
    return{"notes": list(db.values())}

@note_router.get('/notes/{note_id}')
async def get_note_by_id(note_id:str):
    if note_id in db:
        return{"id": note_id, "note": db[note_id]}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail ="Note Not Found")

@note_router.put('/notes/{note_id}')
async def update_note(note_id:str, note_update:UpdateNote):
    for note_id in db:
        updated_note = db[note_id].copy(update={"content": note_update.content})
        db[note_id] = updated_note
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")

@note_router.delete('/notes/{note_id}')
async def delete_note(note_id:str):
    if note_id in db:
            del db[note_id]
            return
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
