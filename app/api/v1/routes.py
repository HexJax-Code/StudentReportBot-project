# app/api/v1/routes.py
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.session import SessionLocal
from app.models.models import Student, Report, SendJob, JobStatus
from pydantic import BaseModel
from app.workers.tasks import enqueue_send_job

router = APIRouter(prefix="/api/v1")

# --- Pydantic schemas
class Grade(BaseModel):
    subject: str
    grade: str

class StudentCreate(BaseModel):
    student_id: str
    full_name: str
    phone: str
    guardian_name: Optional[str] = None
    grades: Optional[List[Grade]] = []

class StudentOut(BaseModel):
    id: int
    student_id: str
    full_name: str
    phone: str
    guardian_name: Optional[str]

    class Config:
        orm_mode = True

class ReportOut(BaseModel):
    id: int
    student_id: int
    report_url: str

    class Config:
        orm_mode = True

class SendJobOut(BaseModel):
    id: int
    report_id: int
    phone: str
    attempt_count: int
    status: JobStatus
    last_error: Optional[str]

    class Config:
        orm_mode = True

# --- DB dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- Students CRUD
@router.post("/students/", response_model=StudentOut, status_code=status.HTTP_201_CREATED)
def create_or_update_student(payload: StudentCreate, db: Session = Depends(get_db)):
    existing = db.query(Student).filter(Student.student_id == payload.student_id).first()
    if existing:
        existing.full_name = payload.full_name
        existing.phone = payload.phone
        existing.guardian_name = payload.guardian_name
        db.add(existing)
        db.commit()
        db.refresh(existing)
        student = existing
    else:
        student = Student(
            student_id=payload.student_id,
            full_name=payload.full_name,
            phone=payload.phone,
            guardian_name=payload.guardian_name
        )
        db.add(student)
        db.commit()
        db.refresh(student)

    # enqueue job for generating + sending report (payload contains grades)
    enqueue_send_job(student.id, payload.dict())
    return student

@router.get("/students/{student_id}", response_model=StudentOut)
def get_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

@router.get("/students/", response_model=List[StudentOut])
def list_students(limit: int = 100, db: Session = Depends(get_db)):
    students = db.query(Student).limit(limit).all()
    return students

@router.delete("/students/{student_id}", status_code=204)
def delete_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    db.delete(student)
    db.commit()
    return

# --- Reports listing
@router.get("/reports/", response_model=List[ReportOut])
def list_reports(limit: int = 100, db: Session = Depends(get_db)):
    return db.query(Report).limit(limit).all()

# --- Send jobs listing and retry
@router.get("/sendjobs/", response_model=List[SendJobOut])
def list_sendjobs(limit: int = 100, db: Session = Depends(get_db)):
    return db.query(SendJob).limit(limit).all()

@router.post("/sendjobs/{job_id}/retry", response_model=SendJobOut)
def retry_sendjob(job_id: int, db: Session = Depends(get_db)):
    job = db.query(SendJob).filter(SendJob.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="SendJob not found")
    # Enqueue again for idempotent retry
    enqueue_send_job(job.report.student.id, None)
    job.status = JobStatus.pending
    job.attempt_count = 0
    db.add(job)
    db.commit()
    db.refresh(job)
    return job
