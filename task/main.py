from fastapi import FastAPI
from user import models
from user.database import engine
from user.router import CompetitionEntry, Competition, user

app = FastAPI()

# Create database tables
models.Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(user.router)
app.include_router(Competition.router)
app.include_router(CompetitionEntry.router)
# app.include_router(participant.router)
