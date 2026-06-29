from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from typing import Literal

from datetime import date, timedelta

from app.schemas.glucose_records_schema import (
    GlucoseRecordBase,
    GlucoseRecordResponse,
    GlucoseSummaryResponse,
)
from app.db.database import get_db
from app.models.glucose_records_model import GlucoseRecord
from app.core.security import get_current_user
from app.models.users_model import User

router = APIRouter(prefix="/glucose-records")


@router.post("/", response_model=GlucoseRecordResponse)
def create_glucose_record(
    record: GlucoseRecordBase,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    new_record = GlucoseRecord(
        date=record.date,
        time=record.time,
        glucose_value=record.glucose_value,
        notes=record.notes,
        user_id=current_user.id,
        moment_of_day=record.moment_of_day,
    )

    db.add(new_record)
    db.commit()
    db.refresh(new_record)

    return new_record


################


@router.get("/summary", response_model=GlucoseSummaryResponse)
def read_summary(
    moment_of_day: (
        Literal["fasting", "before_meal", "after_meal", "night", "other"] | None
    ) = None,
    start_date: date | None = None,
    end_date: date | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    query = db.query(GlucoseRecord).filter(GlucoseRecord.user_id == current_user.id)

    if current_user.subscription_type == "standard":
        oldest_allowed_date = date.today() - timedelta(days=30)
        query = query.filter(GlucoseRecord.date >= oldest_allowed_date)
    if moment_of_day:
        query = query.filter(GlucoseRecord.moment_of_day == moment_of_day)
    if start_date is not None:
        query = query.filter(GlucoseRecord.date >= start_date)
    if end_date is not None:
        query = query.filter(GlucoseRecord.date <= end_date)

    glucemias = query.order_by(GlucoseRecord.date, GlucoseRecord.time).all()

    if not glucemias:
        glucose_summary = GlucoseSummaryResponse(
            total_records=0,
            min_glucemia=None,
            max_glucemia=None,
            average_glucemia=None,
            last_glucemia=None,
        )
        return glucose_summary

    min_glucemia = min(glucemias, key=lambda glucosa: glucosa.glucose_value)
    max_glucemia = max(glucemias, key=lambda glucosa: glucosa.glucose_value)

    glucose_summary = GlucoseSummaryResponse(
        total_records=len(glucemias),
        min_glucemia=min_glucemia,
        max_glucemia=max_glucemia,
        average_glucemia=round(
            sum(glucosa.glucose_value for glucosa in glucemias) / len(glucemias)
        ),
        last_glucemia=glucemias[-1],
    )
    return glucose_summary


#################


@router.delete("/{record_id}")
def delete_glucose_record(
    record_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    oldest_allowed_date = date.today() - timedelta(days=30)
    deleted_record = (
        db.query(GlucoseRecord)
        .filter(GlucoseRecord.id == record_id, GlucoseRecord.user_id == current_user.id)
        .first()
    )

    if deleted_record is None:
        raise HTTPException(status_code=404, detail="Registro no encontrado")
    if (
        current_user.subscription_type == "standard"
        and deleted_record.date < oldest_allowed_date
    ):
        raise HTTPException(status_code=404, detail="Registro no encontrado")

    db.delete(deleted_record)
    db.commit()

    return {"message": "Registro eliminado correctamente"}


################


@router.get("/{record_id}", response_model=GlucoseRecordResponse)
def read_glucose_record_by_id(
    record_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    oldest_allowed_date = date.today() - timedelta(days=30)
    glucose_record = (
        db.query(GlucoseRecord)
        .filter(GlucoseRecord.id == record_id, GlucoseRecord.user_id == current_user.id)
        .first()
    )

    if glucose_record is None:
        raise HTTPException(status_code=404, detail="Registro no encontrado")

    if (
        current_user.subscription_type == "standard"
        and glucose_record.date < oldest_allowed_date
    ):
        raise HTTPException(status_code=404, detail="Registro no encontrado")

    return glucose_record


##################


@router.put("/{record_id}", response_model=GlucoseRecordResponse)
def edit_glucose_record(
    record_id: int,
    glucose_put: GlucoseRecordBase,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    oldest_allowed_date = date.today() - timedelta(days=30)
    glucose_record = (
        db.query(GlucoseRecord)
        .filter(GlucoseRecord.id == record_id, GlucoseRecord.user_id == current_user.id)
        .first()
    )

    if glucose_record is None:
        raise HTTPException(status_code=404, detail="Registro no encontrado")

    if (
        current_user.subscription_type == "standard"
        and glucose_record.date < oldest_allowed_date
    ):
        raise HTTPException(status_code=404, detail="Registro no encontrado")

    glucose_record.date = glucose_put.date
    glucose_record.time = glucose_put.time
    glucose_record.glucose_value = glucose_put.glucose_value
    glucose_record.notes = glucose_put.notes
    glucose_record.moment_of_day = glucose_put.moment_of_day

    db.commit()
    db.refresh(glucose_record)

    return glucose_record



@router.get("/", response_model=list[GlucoseRecordResponse])
def read_glucose_records(
    moment_of_day: (
        Literal["fasting", "before_meal", "after_meal", "night", "other"] | None
    ) = None,
    start_date: date | None = None,
    end_date: date | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    query = db.query(GlucoseRecord).filter(GlucoseRecord.user_id == current_user.id)

    if current_user.subscription_type == "standard":
        oldest_allowed_date = date.today() - timedelta(days=30)
        query = query.filter(GlucoseRecord.date >= oldest_allowed_date)
    if moment_of_day:
        query = query.filter(GlucoseRecord.moment_of_day == moment_of_day)
    if start_date is not None:
        query = query.filter(GlucoseRecord.date >= start_date)
    if end_date is not None:
        query = query.filter(GlucoseRecord.date <= end_date)
    return query.order_by(GlucoseRecord.date, GlucoseRecord.time).all()


##################################
