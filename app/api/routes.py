from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.tasks import enqueue_report_job

router = APIRouter(prefix="/api")

class StudentInput(BaseModel):
    name: str
    phone: str
    math: int
    english: int
    science: int

@router.post("/student/report")
def create_report(student: StudentInput):
    try:
        enqueue_report_job(student.dict())
        return {"status": "queued", "student": student.name}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
