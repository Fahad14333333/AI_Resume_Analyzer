# AI Resume Analyzer

A production-ready AI Resume Analyzer full-stack application built with FastAPI, React, TailwindCSS, PostgreSQL, and modern NLP techniques.

## Features

- Resume upload with PDF/DOCX support
- OCR fallback for scanned resumes
- Intelligent resume parsing for name, email, phone, skills, experience, education, projects, certifications, and languages
- Semantic Job Description matching with `all-MiniLM-L6-v2`
- ATS compatibility scoring, missing skills detection, and fake keyword stuffing identification
- Interview question generation and resume summary generation
- Recruiter dashboard with score meters and skill matching charts
- Multilingual support including English + Urdu
- Secure uploads, validation, file size checks, and rate limiting
- Docker and GitHub Actions deployment support

## Folder structure

- `backend/`: FastAPI backend, NLP services, database models, and Docker container.
- `frontend/`: React + Vite frontend UI with TailwindCSS.
- `docs/`: Architecture and API documentation.
- `example_data/`: Sample resume and job description files.

## Setup Guide

### Backend

1. Install Python dependencies:
   ```bash
   cd backend
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   python -m spacy download en_core_web_sm
   ```
2. Start the backend service:
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

### Frontend

1. Install Node dependencies:
   ```bash
   cd frontend
   npm install
   ```
2. Start the frontend dev server:
   ```bash
   npm run dev
   ```

## Deployment

Use Docker Compose to run the full stack locally:

```bash
docker compose up --build
```

## API Endpoints

- `GET /api/health`
- `POST /api/v1/upload-resume`
- `POST /api/v1/analyze`
- `POST /api/v1/rank`
- `POST /api/v1/summary`

## Notes

- The backend uses spaCy for entity extraction and SentenceTransformers for semantic matching.
- The frontend UI is designed with glassmorphism styling, responsive layout, and animated score meters.
- The repository is optimized for portfolio presentation and internship applications.
