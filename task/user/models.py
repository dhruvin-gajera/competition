from sqlalchemy import Column, String, Integer, DateTime, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID

from sqlalchemy.orm import relationship
from user.database import Base
import uuid
from datetime import datetime

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)  # Integer ID
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String)
    age = Column(Integer, nullable=False)
    gender = Column(String(50), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    modified_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_deleted = Column(Boolean, default=False)

    # Relationships
    entries = relationship("CompetitionEntry", back_populates="user")
class Competition(Base):
    __tablename__ = 'competitions'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)  # Integer ID
    competition_name = Column(String(255), nullable=False)
    competition_date = Column(DateTime, nullable=False)
    duration = Column(Integer, nullable=False)  # Duration in hours or days
    user_capacity = Column(Integer, nullable=False)  # Max number of users allowed
    created_at = Column(DateTime, default=datetime.utcnow)
    modified_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_deleted = Column(Boolean, default=False)

    # Relationships
    entries = relationship("CompetitionEntry", back_populates="competition")


class CompetitionEntry(Base):
    __tablename__ = 'competition_entries'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)  # Integer ID
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    competition_id = Column(Integer, ForeignKey('competitions.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    modified_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_deleted = Column(Boolean, default=False)

    # Relationships
    user = relationship("User", back_populates="entries")
    competition = relationship("Competition", back_populates="entries")