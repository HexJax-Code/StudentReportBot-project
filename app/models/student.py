from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    math = Column(Integer)
    english = Column(Integer)
    science = Column(Integer)
    pdf_path = Column(String, nullable=True)
