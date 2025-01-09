from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from user import models, schema
from user.database import get_db
from uuid import uuid4

router = APIRouter(prefix="/users", tags=["User"])

# Create a new user
@router.post("/", response_model=schema.UserBase)
def create_user(user: schema.UserCreate, db: Session = Depends(get_db)):
    new_user = models.User(
        id=user.id,  # Generate UUID as a string for the id
        name=user.name,
        email=user.email,
        password=user.password,  # Remember to hash the password
        age=user.age,
        gender=user.gender,
    )
    db.add(new_user)
    db.commit() 
    db.refresh(new_user) 
    print(new_user.id)
    return new_user

# Read all users
@router.get("/", response_model=list[schema.UserBase])
def get_all_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()


# Read a specific user by ID
@router.get("/{user_id}", response_model=schema.UserBase)
def get_user(user_id: str, db: Session = Depends(get_db)):
    try:
        user_uuid = UUID(user_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid UUID format")
    
    user = db.query(models.User).filter(models.User.id == user_uuid).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# Update a user
@router.put("/{user_id}", response_model=schema.UserBase)
def update_user(user_id: str, user: schema.UserUpdate, db: Session = Depends(get_db)):

    
    
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    db_user.name = user.name if user.name else db_user.name
    db_user.email = user.email if user.email else db_user.email
    db_user.age = user.age if user.age else db_user.age
    db_user.gender = user.gender if user.gender else db_user.gender
    db_user.password = user.password if user.password else db_user.password  # You should hash the password before saving it in production
    db.commit()
    db.refresh(db_user)
    return db_user


from uuid import UUID

@router.delete("/{user_id}")
def delete_user(user_id: str, db: Session = Depends(get_db)):
    
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"message": f"User with ID {user_id} deleted successfully"}
