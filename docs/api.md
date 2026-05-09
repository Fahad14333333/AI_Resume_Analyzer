# API Documentation

## Endpoints

### GET /api/health
Returns the health status of the service.

### POST /api/v1/upload-resume
Accepts a resume upload and optional job description.

Request:
- file: PDF or DOCX resume
- job_description: optional text field

Response:
- filename
- content_preview
- parsed_resume
- analysis

### POST /api/v1/analyze
Accepts resume text and job description JSON to return a full analysis.

Request body:
- resume_text
- job_description

### POST /api/v1/rank
Ranks multiple resumes against one job description.

Request body:
- resumes: list of { filename, resume_text }
- job_description

### POST /api/v1/summary
Generates a professional resume summary and interview questions.

Request body:
- resume_text
- job_description (optional)
