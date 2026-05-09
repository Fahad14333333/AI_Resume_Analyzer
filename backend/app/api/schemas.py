from typing import List, Optional
from pydantic import BaseModel, Field

class ResumeItem(BaseModel):
    filename: str
    resume_text: str

class AnalyzeRequest(BaseModel):
    resume_text: str = Field(..., description="The text extracted from the resume.")
    job_description: str = Field(..., description="The job description text for comparison.")

class RankRequest(BaseModel):
    resumes: List[ResumeItem]
    job_description: str

class SummaryRequest(BaseModel):
    resume_text: str
    job_description: Optional[str] = None

class EntityMatch(BaseModel):
    label: str
    text: str
    confidence: float

class ResumeProfile(BaseModel):
    name: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    skills: List[str] = []
    experience: List[str] = []
    education: List[str] = []
    certifications: List[str] = []
    projects: List[str] = []
    languages: List[str] = []
    summary: Optional[str]

class AnalysisMetrics(BaseModel):
    ats_score: float
    semantic_similarity: float
    skill_match_rate: float
    missing_skills: List[str]
    keyword_stuffing: bool
    confidence: float
    grammar_score: float
    explainable: dict

class UploadResponse(BaseModel):
    filename: str
    content_preview: str
    parsed_resume: ResumeProfile
    analysis: AnalysisMetrics

class AnalyzeResponse(BaseModel):
    parsed_resume: ResumeProfile
    analysis: AnalysisMetrics

class RankedResume(BaseModel):
    filename: str
    score: float
    analysis: AnalysisMetrics

class RankResponse(BaseModel):
    ranked_resumes: List[RankedResume]

class SummaryResponse(BaseModel):
    summary: str
    interview_questions: List[str]
