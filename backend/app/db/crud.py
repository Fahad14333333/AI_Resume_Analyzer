from sqlalchemy.orm import Session
from app.db import models


def create_resume(db: Session, filename: str, raw_text: str, analysis: str, score: float, name: str = None, email: str = None, phone: str = None):
    record = models.Resume(
        filename=filename,
        raw_text=raw_text,
        analysis=analysis,
        score=score,
        name=name,
        email=email,
        phone=phone,
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


def create_job_description(db: Session, title: str, text: str):
    record = models.JobDescription(title=title, text=text)
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


def create_analysis_report(db: Session, resume_id: int, job_description_id: int, report: str, score: float):
    record = models.AnalysisReport(
        resume_id=resume_id,
        job_description_id=job_description_id,
        report=report,
        score=score,
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record
