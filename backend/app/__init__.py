from fastapi import FastAPI, status
from app.routes import note_router

version = "v1"

app = FastAPI(
    title="Soap_Note",
    description="A soap note taker for massage therapists",
    version= version
)

app.include_router(note_router, prefix=f'/api/{version}/', tags=['notes'])