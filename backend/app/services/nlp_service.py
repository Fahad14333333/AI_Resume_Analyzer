import re
from typing import List, Dict
import numpy as np
import spacy
from sentence_transformers import SentenceTransformer
from sklearn.feature_extraction.text import TfidfVectorizer

from app.core.config import settings


class NLPService:
    model = None
    nlp = None
    skill_ontology = None

    @classmethod
    def initialize(cls):
        if cls.model is None:
            cls.model = SentenceTransformer(settings.EMBEDDING_MODEL)
        if cls.nlp is None:
            try:
                cls.nlp = spacy.load("en_core_web_sm")
            except OSError:
                cls.nlp = spacy.blank("en")

    @classmethod
    def shutdown(cls):
        cls.model = None
        cls.nlp = None

    @classmethod
    def clean_text(cls, text: str) -> str:
        cleaned = re.sub(r"\s+", " ", text).strip()
        cleaned = re.sub(r"[^\w\s\u0600-\u06FF@.,:/+-]", " ", cleaned)
        return cleaned

    @classmethod
    def generate_embeddings(cls, text: str) -> List[float]:
        cls.initialize()
        return cls.model.encode(text, convert_to_numpy=True).tolist()

    @classmethod
    def cosine_similarity(cls, vector_a, vector_b) -> float:
        a = np.array(vector_a, dtype=float)
        b = np.array(vector_b, dtype=float)
        if np.linalg.norm(a) == 0 or np.linalg.norm(b) == 0:
            return 0.0
        return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))

    @classmethod
    def extract_keywords(cls, text: str, top_n: int = 8) -> List[str]:
        cleaned = cls.clean_text(text).lower()
        tokens = [token for token in re.split(r"\W+", cleaned) if len(token) > 2]
        freq = {}
        for token in tokens:
            freq[token] = freq.get(token, 0) + 1
        sorted_tokens = sorted(freq.items(), key=lambda item: (-item[1], item[0]))
        return [item[0] for item in sorted_tokens[:top_n]]

    @classmethod
    def get_skill_ontology(cls) -> List[str]:
        if cls.skill_ontology is None:
            cls.skill_ontology = [
                "Python", "Java", "C++", "SQL", "PostgreSQL", "Machine Learning", "NLP",
                "Docker", "Kubernetes", "AWS", "Azure", "TensorFlow", "PyTorch", "spaCy",
                "Git", "React", "Node.js", "Data Analysis", "Communication", "Project Management",
                "Excel", "Tableau", "Power BI", "Agile", "Scrum", "Automation",
            ]
        return cls.skill_ontology

    @classmethod
    def detect_language(cls, text: str) -> str:
        if re.search(r"[\u0600-\u06FF]", text):
            return "ur"
        return "en"

    @classmethod
    def ner_entities(cls, text: str) -> List[Dict[str, float]]:
        cls.initialize()
        doc = cls.nlp(text)
        return [{"text": ent.text, "label": ent.label_, "confidence": 0.8} for ent in doc.ents]

    @classmethod
    def grammar_score(cls, text: str) -> float:
        sentences = re.split(r"[.!?]", text)
        sentence_count = max(1, len([s for s in sentences if s.strip()]))
        words = text.split()
        punctuation = len(re.findall(r"[.!?]", text))
        score = max(0.0, min(1.0, (punctuation + 0.1 * len(words)) / (sentence_count * 10)))
        return round(score * 100, 1)

    @classmethod
    def generate_resume_summary(cls, parsed_resume: Dict, job_description: str = "") -> str:
        skills = ", ".join(parsed_resume.get("skills", [])[:6])
        experience_count = len(parsed_resume.get("experience", []))
        education_count = len(parsed_resume.get("education", []))
        jd_snippet = job_description[:160].strip()
        return (
            f"Experienced professional with {experience_count} resume sections and {education_count} education entries. "
            f"Core skills include {skills}. "
            f"This resume is matched against the role requirements: {jd_snippet}."
        ).strip()

    @classmethod
    def generate_interview_questions(cls, parsed_resume: Dict, job_description: str = "") -> List[str]:
        questions = []
        if parsed_resume.get("skills"):
            for skill in parsed_resume["skills"][:4]:
                questions.append(f"Can you describe a project where you used {skill} and what impact you achieved?")
        if parsed_resume.get("projects"):
            questions.append("Tell me about your most significant project and the tools you used.")
        if job_description:
            questions.append("How would you apply your experience to solve a key challenge described in this job posting?")
        return questions[:8]

    @classmethod
    def semantic_match(cls, resume_text: str, job_description: str) -> float:
        cls.initialize()
        resume_vector = cls.generate_embeddings(resume_text)
        jd_vector = cls.generate_embeddings(job_description)
        return cls.cosine_similarity(resume_vector, jd_vector)
