from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from app.api.schemas import AnalyzeRequest, AnalyzeResponse, RankRequest, RankResponse, UploadResponse, SummaryRequest, SummaryResponse
from app.services.file_service import FileService
from app.services.parser_service import ParserService
from app.services.scoring_service import ScoringService
from app.services.nlp_service import NLPService

router = APIRouter()

@router.get("/health")
def health_check():
    return {"status": "ok", "version": "0.1.0"}

@router.post("/v1/upload-resume", response_model=UploadResponse)
async def upload_resume(file: UploadFile = File(...), job_description: str = Form("")):
    text = await FileService.extract_resume_text(file)
    if not text.strip():
        raise HTTPException(status_code=422, detail="Uploaded file contains no readable text.")

    parsed = ParserService.parse_resume(text)
    if job_description:
        analysis = ScoringService.compare_resume_to_jd(parsed, job_description)
    else:
        analysis = ScoringService.quick_report(parsed)

    return {
        "filename": file.filename,
        "content_preview": text[:1200],
        "parsed_resume": parsed,
        "analysis": analysis,
    }

@router.post("/v1/analyze", response_model=AnalyzeResponse)
def analyze_resume(payload: AnalyzeRequest):
    parsed = ParserService.parse_resume(payload.resume_text)
    analysis = ScoringService.compare_resume_to_jd(parsed, payload.job_description)
    return {"parsed_resume": parsed, "analysis": analysis}

@router.post("/v1/rank", response_model=RankResponse)
def rank_resumes(payload: RankRequest):
    ranked = []
    for item in payload.resumes:
        parsed = ParserService.parse_resume(item.resume_text)
        analysis = ScoringService.compare_resume_to_jd(parsed, payload.job_description)
        ranked.append({"filename": item.filename, "score": analysis["ats_score"], "analysis": analysis})
    ranked.sort(key=lambda item: item["score"], reverse=True)
    return {"ranked_resumes": ranked}

@router.post("/v1/summary", response_model=SummaryResponse)
def summary(payload: SummaryRequest):
    parsed = ParserService.parse_resume(payload.resume_text)
    summary_text = NLPService.generate_resume_summary(parsed, payload.job_description)
    questions = NLPService.generate_interview_questions(parsed, payload.job_description)
    return {"summary": summary_text, "interview_questions": questions}
