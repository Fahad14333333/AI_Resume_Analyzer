import re
from typing import List, Dict
from app.services.nlp_service import NLPService

SECTION_KEYWORDS = {
    "experience": ["experience", "employment", "work history", "professional experience"],
    "education": ["education", "academic", "qualifications", "degree"],
    "skills": ["skills", "technical skills", "expertise"],
    "projects": ["projects", "project experience"],
    "certifications": ["certifications", "licenses", "credentials"],
    "languages": ["languages", "language"],
}

PHONE_PATTERN = re.compile(r"\+?\d[\d\s\-()]{7,}\d")
EMAIL_PATTERN = re.compile(r"[\w\.-]+@[\w\.-]+\.[a-zA-Z]{2,}")
NAME_PATTERN = re.compile(r"^[A-Z][a-z]+(?:\s[A-Z][a-z]+){0,3}$")


class ParserService:
    @staticmethod
    def parse_resume(text: str) -> Dict:
        text = text.strip()
        sections = ParserService._split_sections(text)
        contact = ParserService._extract_contact(text)
        skills = ParserService._extract_skills(text)
        experience = ParserService._extract_section_lines(sections.get("experience", []))
        education = ParserService._extract_section_lines(sections.get("education", []))
        projects = ParserService._extract_section_lines(sections.get("projects", []))
        certifications = ParserService._extract_section_lines(sections.get("certifications", []))
        languages = ParserService._extract_languages(text)
        summary = NLPService.extract_keywords(text, top_n=6)

        return {
            "name": contact.get("name"),
            "email": contact.get("email"),
            "phone": contact.get("phone"),
            "skills": skills,
            "experience": experience,
            "education": education,
            "projects": projects,
            "certifications": certifications,
            "languages": languages,
            "summary": " ".join(summary),
            "raw_text": text,
        }

    @staticmethod
    def _split_sections(text: str) -> Dict[str, List[str]]:
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        current_section = "others"
        sections = {"experience": [], "education": [], "skills": [], "projects": [], "certifications": [], "languages": []}
        for line in lines:
            lowered = line.lower()
            for section, keywords in SECTION_KEYWORDS.items():
                if any(keyword in lowered for keyword in keywords):
                    current_section = section
                    break
            sections.setdefault(current_section, []).append(line)
        return sections

    @staticmethod
    def _extract_contact(text: str) -> Dict[str, str]:
        contact = {}
        email = EMAIL_PATTERN.search(text)
        phone = PHONE_PATTERN.search(text)
        contact["email"] = email.group(0) if email else None
        contact["phone"] = phone.group(0) if phone else None
        for line in text.splitlines():
            cleaned = line.strip()
            if cleaned and NAME_PATTERN.match(cleaned) and len(cleaned.split()) <= 4:
                contact["name"] = cleaned
                break
        return contact

    @staticmethod
    def _extract_skills(text: str) -> List[str]:
        skill_list = NLPService.get_skill_ontology()
        found = set()
        lower_text = text.lower()
        for skill in skill_list:
            if skill.lower() in lower_text:
                found.add(skill)
        return sorted(found)

    @staticmethod
    def _extract_section_lines(lines: List[str]) -> List[str]:
        cleaned = []
        for line in lines:
            if len(line) > 10:
                cleaned.append(line)
        return cleaned[:12]

    @staticmethod
    def _extract_languages(text: str) -> List[str]:
        language_keywords = ["english", "urdu", "hindi", "spanish", "french", "arabic", "german"]
        found = [lang.title() for lang in language_keywords if lang in text.lower()]
        return found
