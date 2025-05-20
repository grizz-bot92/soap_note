from pydantic import BaseModel

db = {}

class NoteIn(BaseModel):
    name: str
    treatment: str
    duration: int
    content: str

class Note(NoteIn):
    id: str

class UpdateNote(BaseModel):
    content: str