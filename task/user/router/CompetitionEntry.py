from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from user import models, schema
from user.database import get_db

class CompetitionEntryWithDetails(schema.CompetitionEntryBase):
    competition_name: str
    empty_positions: int  # The number of empty positions available

router = APIRouter(prefix="/competition-entries", tags=["CompetitionEntry"])

@router.post("/", response_model=CompetitionEntryWithDetails)
def create_competition_entry(
    entry: schema.CompetitionEntryCreate, db: Session = Depends(get_db)
):
    user = db.query(models.User).filter(models.User.id == entry.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    competition = db.query(models.Competition).filter(models.Competition.id == entry.competition_id).first()
    if not competition:
        raise HTTPException(status_code=404, detail="Competition not found")

    current_entries_count = db.query(models.CompetitionEntry).filter(models.CompetitionEntry.competition_id == entry.competition_id).count()
    if current_entries_count >= competition.user_capacity:
        raise HTTPException(status_code=400, detail="Competition is full")

    new_entry = models.CompetitionEntry(
        user_id=entry.user_id,
        competition_id=entry.competition_id,
    )
    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)

    empty_positions = competition.user_capacity - current_entries_count - 1  # Remaining positions after the new entry

    # Include the competition name and the number of empty positions in the response
    return {
        **new_entry.__dict__,  # Keep all fields from the new entry
        "competition_name": competition.competition_name,
        "empty_positions": empty_positions
    }

# Read all competition entries
@router.get("/", response_model=list[schema.CompetitionEntryBase])
def get_all_competition_entries(db: Session = Depends(get_db)):
    return db.query(models.CompetitionEntry).all()


# Read a specific competition entry by ID
# @router.get("/{entry_id}", response_model=schema.CompetitionEntryBase)
# def get_competition_entry(entry_id: str, db: Session = Depends(get_db)):
#     entry = db.query(models.CompetitionEntry).filter(models.CompetitionEntry.id == entry_id).first()
#     if not entry:
#         raise HTTPException(status_code=404, detail="Competition Entry not found")
#     return entry


# Update a competition entry
@router.put("/{entry_id}", response_model=schema.CompetitionEntryBase)
def update_competition_entry(
    entry_id: str, entry: schema.CompetitionEntryUpdate, db: Session = Depends(get_db)
):
    db_entry = db.query(models.CompetitionEntry).filter(models.CompetitionEntry.id == entry_id).first()
    if not db_entry:
        raise HTTPException(status_code=404, detail="Competition Entry not found")

    db_entry.is_deleted = entry.is_deleted if entry.is_deleted is not None else db_entry.is_deleted
    db.commit()
    db.refresh(db_entry)
    return db_entry


# Delete a competition entry
@router.delete("/{entry_id}")
def delete_competition_entry(entry_id: str, db: Session = Depends(get_db)):
    entry = db.query(models.CompetitionEntry).filter(models.CompetitionEntry.id == entry_id).first()
    if not entry:
        raise HTTPException(status_code=404, detail="Competition Entry not found")
    db.delete(entry)
    db.commit()
    return {"message": f"Competition Entry with ID {entry_id} deleted successfully"}
