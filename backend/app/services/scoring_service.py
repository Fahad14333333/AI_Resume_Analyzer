from typing import Dict, List
from collections import Counter

from app.services.nlp_service import NLPService


class ScoringService:
    @staticmethod
    def compare_resume_to_jd(parsed_resume: Dict, job_description: str) -> Dict:
        resume_text = parsed_resume.get("raw_text", "")
        skills = parsed_resume.get("skills", [])
        job_skills = [skill for skill in NLPService.extract_keywords(job_description, top_n=20)]
        semantic_similarity = NLPService.semantic_match(resume_text, job_description)
        matched_skills = [skill for skill in skills if skill.lower() in job_description.lower()]
        missing_skills = [skill for skill in job_skills if skill.lower() not in [s.lower() for s in skills]]
        keyword_stuffing = ScoringService.detect_keyword_stuffing(resume_text)
        grammar_score = NLPService.grammar_score(resume_text)
        ats_score = round(
            (len(matched_skills) / max(1, len(job_skills))) * 0.6
            + semantic_similarity * 0.3
            + (grammar_score / 100) * 0.1,
            2,
        )
        confidence = round((semantic_similarity + len(matched_skills) / max(1, len(job_skills))) / 2, 2)
        explainable = {
            "matched_skills": matched_skills,
            "detected_job_skills": job_skills,
            "skill_gap": missing_skills,
            "semantic_similarity": round(semantic_similarity, 2),
            "keyword_stuffing": keyword_stuffing,
        }
        return {
            "ats_score": round(min(max(ats_score * 100, 0), 100), 1),
            "semantic_similarity": round(semantic_similarity * 100, 1),
            "skill_match_rate": round(len(matched_skills) / max(1, len(job_skills)) * 100, 1),
            "missing_skills": missing_skills[:12],
            "keyword_stuffing": keyword_stuffing,
            "confidence": confidence,
            "grammar_score": grammar_score,
            "explainable": explainable,
        }

    @staticmethod
    def quick_report(parsed_resume: Dict) -> Dict:
        resume_text = parsed_resume.get("raw_text", "")
        grammar_score = NLPService.grammar_score(resume_text)
        skills = parsed_resume.get("skills", [])
        return {
            "ats_score": 0.0,
            "semantic_similarity": 0.0,
            "skill_match_rate": round(len(skills) / max(1, len(NLPService.get_skill_ontology())) * 100, 1),
            "missing_skills": [],
            "keyword_stuffing": ScoringService.detect_keyword_stuffing(resume_text),
            "confidence": 0.7,
            "grammar_score": grammar_score,
            "explainable": {
                "skill_count": len(skills),
                "grammar_score": grammar_score,
            },
        }

    @staticmethod
    def detect_keyword_stuffing(text: str) -> bool:
        words = [word.lower() for word in text.split() if len(word) > 3]
        counts = Counter(words)
        return any(count > 12 for count in counts.values())
