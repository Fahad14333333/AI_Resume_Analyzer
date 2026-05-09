import time

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

from app.api.routes import router
from app.services.nlp_service import NLPService
from app.core.config import settings

# Skip database initialization for demo
# Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI Resume Analyzer",
    description="A production-ready AI resume analyzer with job description matching and recruiter dashboard analytics.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

RATE_LIMIT = {}
MAX_REQUESTS_PER_MINUTE = 45
WINDOW_SECONDS = 60

@app.middleware("http")
async def rate_limiter(request: Request, call_next):
    client_ip = request.client.host
    now = time.time()
    request_times = RATE_LIMIT.setdefault(client_ip, [])
    request_times[:] = [timestamp for timestamp in request_times if timestamp + WINDOW_SECONDS > now]
    if len(request_times) >= MAX_REQUESTS_PER_MINUTE:
        return JSONResponse(status_code=429, content={"detail": "Rate limit exceeded."})
    request_times.append(now)
    return await call_next(request)

@app.on_event("startup")
def startup_event():
    NLPService.initialize()

@app.on_event("shutdown")
def shutdown_event():
    NLPService.shutdown()

app.include_router(router, prefix="/api")
