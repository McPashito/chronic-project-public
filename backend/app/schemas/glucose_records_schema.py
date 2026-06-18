from pydantic import BaseModel, ConfigDict, Field, field_validator
from datetime import date, time, datetime
from typing import Literal


class GlucoseRecordBase(BaseModel):
    date: date
    time: time
    glucose_value: int = Field(ge=20, le=600)
    notes: str | None = Field(default=None, max_length=255)
    moment_of_day: Literal["fasting", "before_meal", "after_meal", "night", "other"]

    @field_validator("date")
    @classmethod
    def date_cannot_be_in_future(cls, value):
        if value > date.today():
            raise ValueError("La fecha de la medición no puede ser futura")
        return value


class GlucoseRecordResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    date: date
    time: time
    glucose_value: int
    notes: str | None = None
    moment_of_day: (
        Literal["fasting", "before_meal", "after_meal", "night", "other"] | None
    ) = None
    created_at: datetime
    updated_at: datetime


class GlucoseSummaryResponse(BaseModel):

    total_records: int
    min_glucemia: GlucoseRecordResponse | None
    max_glucemia: GlucoseRecordResponse | None
    average_glucemia: int | None
    last_glucemia: GlucoseRecordResponse | None
