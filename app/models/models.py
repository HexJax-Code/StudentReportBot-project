# app/models/models.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum, Text
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql import func
import enum

Base = declarative_base()

class JobStatus(str, enum.Enum):
    pending = "pending"
    sent = "sent"
    failed = "failed"
    delivered = "delivered"

class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(String(64), unique=True, nullable=False, index=True)
    full_name = Column(String(256), nullable=False)
    phone = Column(String(64), nullable=False)
    guardian_name = Column(String(256), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    reports = relationship("Report", back_populates="student", cascade="all, delete-orphan")

class Report(Base):
    __tablename__ = "reports"
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    report_url = Column(String(1024), nullable=False)
    generated_at = Column(DateTime(timezone=True), server_default=func.now())

    student = relationship("Student", back_populates="reports")

class SendJob(Base):
    __tablename__ = "send_jobs"
    id = Column(Integer, primary_key=True, index=True)
    report_id = Column(Integer, ForeignKey("reports.id", ondelete="CASCADE"), nullable=False)
    phone = Column(String(64), nullable=False)
    attempt_count = Column(Integer, default=0)
    status = Column(Enum(JobStatus), default=JobStatus.pending)
    last_error = Column(Text, nullable=True)
    scheduled_for = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    report = relationship("Report")
