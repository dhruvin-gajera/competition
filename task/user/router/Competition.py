from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from user import models, schema
from user.database import get_db

router = APIRouter(prefix="/competitions", tags=["Competition"])

# Create a new competition
@router.post("/", response_model=schema.CompetitionBase)
def create_competition(
    competition: schema.CompetitionCreate, db: Session = Depends(get_db)
):
    new_competition = models.Competition(
        competition_name=competition.competition_name,
        competition_date=competition.competition_date,
        duration=competition.duration,
        user_capacity=competition.user_capacity,
    )
    db.add(new_competition)
    db.commit()
    db.refresh(new_competition)
    return new_competition


# Read all competitions
@router.get("/", response_model=list[schema.CompetitionBase])
def get_all_competitions(db: Session = Depends(get_db)):
    return db.query(models.Competition).all()


# Read a specific competition by ID
@router.get("/{competition_id}", response_model=schema.CompetitionBase)
def get_competition(competition_id: str, db: Session = Depends(get_db)):
    competition = db.query(models.Competition).filter(models.Competition.id == competition_id).first()
    if not competition:
        raise HTTPException(status_code=404, detail="Competition not found")
    return competition


# Update a competition
@router.put("/{competition_id}", response_model=schema.CompetitionBase)
def update_competition(
    competition_id: str, competition: schema.CompetitionUpdate, db: Session = Depends(get_db)
):
    db_competition = db.query(models.Competition).filter(models.Competition.id == competition_id).first()
    if not db_competition:
        raise HTTPException(status_code=404, detail="Competition not found")

    db_competition.competition_name = competition.competition_name if competition.competition_name else db_competition.competition_name
    db_competition.competition_date = competition.competition_date if competition.competition_date else db_competition.competition_date
    db_competition.duration = competition.duration if competition.duration else db_competition.duration
    db_competition.user_capacity = competition.user_capacity if competition.user_capacity else db_competition.user_capacity
    db.commit()
    db.refresh(db_competition)
    return db_competition


# Delete a competition
@router.delete("/{competition_id}")
def delete_competition(competition_id: str, db: Session = Depends(get_db)):
    competition = db.query(models.Competition).filter(models.Competition.id == competition_id).first()
    if not competition:
        raise HTTPException(status_code=404, detail="Competition not found")
    db.delete(competition)
    db.commit()
    return {"message": f"Competition with ID {competition_id} deleted successfully"}
