from datetime import datetime, timezone

from sqlalchemy import Column, Integer, String, Date, Time, DateTime, ForeignKey
from app.db.database import Base


class GlucoseRecord(Base):
    __tablename__ = "glucose_records"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    date = Column(Date, nullable=False)
    time = Column(Time, nullable=False)
    glucose_value = Column(Integer, nullable=False)
    notes = Column(String, nullable=True)
    moment_of_day = Column(String, nullable=True)

    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
