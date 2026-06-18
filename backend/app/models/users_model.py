from datetime import datetime, timezone

from sqlalchemy import Column, Integer, String, Date, DateTime
from app.db.database import Base

class User(Base):
    __tablename__ = "users"

    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password= Column(String, nullable=False)
    name= Column(String, nullable=False)
    surname= Column(String, nullable=False)
    date_of_birth = Column(Date, nullable=False)
    subscription_type= Column(String, default="standard", nullable=False)
    created_at= Column(
      DateTime(timezone=True),
      default=lambda: datetime.now(timezone.utc),
      nullable=False
    )
    updated_at= Column(
      DateTime(timezone=True),
      default=lambda: datetime.now(timezone.utc),
      onupdate=lambda: datetime.now(timezone.utc),
      nullable=False
      
    )
      
