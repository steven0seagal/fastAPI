from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from diagnostics_lab.api.deps import get_current_user
from diagnostics_lab.db.models.patient import Patient
from diagnostics_lab.db.models.user import User
from diagnostics_lab.db.session import get_db
from diagnostics_lab.schemas.patients import PatientCreate, PatientRead, PatientUpdate

router = APIRouter(prefix="/patients", tags=["patients"])


@router.post("", response_model=PatientRead, status_code=status.HTTP_201_CREATED)
def create_patient(
    payload: PatientCreate,
    db: Session = Depends(get_db),
    _user: User = Depends(get_current_user),
) -> Patient:
    patient = Patient(
        external_id=payload.external_id,
        first_name=payload.first_name,
        last_name=payload.last_name,
        dob=payload.dob,
        sex=payload.sex,
    )
    db.add(patient)
    try:
        db.commit()
    except IntegrityError as err:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Patient already exists"
        ) from err

    db.refresh(patient)
    return patient


@router.get("", response_model=list[PatientRead])
def list_patients(
    limit: int = 50,
    offset: int = 0,
    db: Session = Depends(get_db),
    _user: User = Depends(get_current_user),
) -> list[Patient]:
    limit = max(1, min(limit, 200))
    offset = max(0, offset)

    stmt = select(Patient).order_by(Patient.id.desc()).limit(limit).offset(offset)
    return list(db.scalars(stmt).all())


@router.get("/{patient_id}", response_model=PatientRead)
def get_patient(
    patient_id: int,
    db: Session = Depends(get_db),
    _user: User = Depends(get_current_user),
) -> Patient:
    patient = db.get(Patient, patient_id)
    if not patient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found")
    return patient


@router.patch("/{patient_id}", response_model=PatientRead)
def update_patient(
    patient_id: int,
    payload: PatientUpdate,
    db: Session = Depends(get_db),
    _user: User = Depends(get_current_user),
) -> Patient:
    patient = db.get(Patient, patient_id)
    if not patient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found")

    data = payload.model_dump(exclude_unset=True)
    for k, v in data.items():
        setattr(patient, k, v)

    try:
        db.commit()
    except IntegrityError as err:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Conflict") from err

    db.refresh(patient)
    return patient
