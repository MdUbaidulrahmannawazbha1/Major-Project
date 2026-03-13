"""
Groq AI Service — powers chatbot, career explanation, job recommendations,
skill-gap analysis, and career roadmap using Llama 3 (free tier).

Set GROQ_API_KEY in .env to enable.  Get a free key at https://console.groq.com
"""
import os
import json
import logging

try:
    from groq import Groq
    _groq_available = True
except ImportError:
    _groq_available = False
    _Groq = None
else:
    _Groq = Groq



GROQ_API_KEY = os.getenv('GROQ_API_KEY')
MODEL = os.getenv('GROQ_MODEL', 'llama-3.1-8b-instant')

_client = None


def _get_client():
    global _client
    if not _groq_available or not GROQ_API_KEY:
        return None
    if _client is None:
        assert _Groq is not None
        _client = _Groq(api_key=GROQ_API_KEY)
    return _client


def is_available():
    return _get_client() is not None


def _chat(messages, system_prompt=None, max_tokens=1024):
    client = _get_client()
    if not client:
        return None
    msgs = []
    if system_prompt:
        msgs.append({'role': 'system', 'content': system_prompt})
    msgs.extend(messages)
    try:
        resp = client.chat.completions.create(
            model=MODEL,
            messages=msgs,
            max_tokens=max_tokens,
        )
        return resp.choices[0].message.content
    except Exception as exc:
        logging.error(f'Groq API error: {exc}')
        return None


def _parse_json(raw, opener='{', closer='}'):
    if not raw:
        return None
    try:
        start = raw.find(opener)
        end = raw.rfind(closer) + 1
        if start == -1 or end == 0:
            return None
        return json.loads(raw[start:end])
    except Exception:
        return None


# ---------------------------------------------------------------------------
# 1. Career result explanation
# ---------------------------------------------------------------------------
def explain_career_result(career_path, confidence, skills=None, cgpa=None):
    """Return a plain-language AI explanation of the career prediction."""
    skill_str = ', '.join((skills or [])[:10]) or 'not provided'
    cgpa_str = str(cgpa) if cgpa else 'not provided'
    prompt = (
        f"A student's career assessment predicted '{career_path}' as their best-fit path "
        f"with {confidence * 100:.1f}% confidence. "
        f"Their skills include: {skill_str}. Their CGPA is: {cgpa_str}. "
        "Write 3–4 sentences: explain why this career fits them, highlight a key strength, "
        "and suggest one concrete next step. Be encouraging and specific."
    )
    return _chat(
        [{'role': 'user', 'content': prompt}],
        system_prompt="You are an expert career counselor. Give concise, personalised, encouraging advice.",
        max_tokens=300,
    )


# ---------------------------------------------------------------------------
# 2. AI-generated job recommendations
# ---------------------------------------------------------------------------
def generate_job_recommendations_ai(skills, career_path, cgpa=None):
    """Return a list of 5 AI-generated job dicts, or None on failure."""
    skill_str = ', '.join((skills or [])[:15]) or 'general skills'
    prompt = (
        f"Student targeting '{career_path}' career. Skills: {skill_str}. "
        f"CGPA: {cgpa or 'not specified'}. "
        "Generate exactly 5 realistic job recommendations for 2025. "
        "Return ONLY a JSON array where each element has these keys: "
        "title, company, required_skills (comma-separated string), "
        "match_score (integer 0-100), why_fit (one sentence). "
        "No markdown, no explanation — pure JSON array."
    )
    raw = _chat(
        [{'role': 'user', 'content': prompt}],
        system_prompt="You are a career placement expert. Respond with valid JSON only.",
        max_tokens=900,
    )
    return _parse_json(raw, opener='[', closer=']')


# ---------------------------------------------------------------------------
# 3. AI skill-gap analysis
# ---------------------------------------------------------------------------
def analyze_skill_gap_ai(found_skills, career_path):
    """Return AI-generated skill gaps and course recommendations, or None."""
    skill_str = ', '.join((found_skills or [])[:15]) or 'none identified'
    prompt = (
        f"Student pursuing '{career_path}' has these skills: {skill_str}. "
        "Identify the top 5 missing skills for this career path in 2025. "
        "For each gap suggest one specific, free online course with its platform. "
        'Return ONLY this JSON: {"gaps": [{"skill": str, "course": str, '
        '"platform": str, "urgency": "high|medium|low"}]}. '
        "No extra text."
    )
    raw = _chat(
        [{'role': 'user', 'content': prompt}],
        system_prompt="You are a technical skills expert. Respond with valid JSON only.",
        max_tokens=700,
    )
    return _parse_json(raw)


# ---------------------------------------------------------------------------
# 4. AI career roadmap (month-by-month plan)
# ---------------------------------------------------------------------------
def generate_roadmap_ai(career_path, skills, cgpa=None):
    """Return a 6-month AI roadmap dict, or None on failure."""
    skill_str = ', '.join((skills or [])[:10]) or 'beginner level'
    prompt = (
        f"Create a 6-month career roadmap for a student targeting '{career_path}'. "
        f"Current skills: {skill_str}. CGPA: {cgpa or 'not specified'}. "
        'Return ONLY this JSON: {"months": [{"month": int, "title": str, '
        '"tasks": [str, str, str], "milestone": str}]}. '
        "Include all 6 months. No extra text."
    )
    raw = _chat(
        [{'role': 'user', 'content': prompt}],
        system_prompt="You are a career development coach. Respond with valid JSON only.",
        max_tokens=1400,
    )
    return _parse_json(raw)


# ---------------------------------------------------------------------------
# 5. AI chatbot
# ---------------------------------------------------------------------------
def chatbot_response(query, user_profile=None):
    """Full LLM-powered career counselor. Returns reply string or None."""
    context = ""
    if user_profile:
        parts = [
            f"Career path: {user_profile.get('career_path') or user_profile.get('career_goal') or 'unknown'}",
            f"Education: {user_profile.get('education_level') or 'not specified'}",
            f"Experience: {user_profile.get('experience_level') or 'not specified'}",
            f"Skills: {user_profile.get('skills') or 'not provided'}",
            f"Interests: {user_profile.get('interests') or 'not provided'}",
            f"CGPA: {user_profile.get('cgpa') or 'not provided'}",
        ]
        context = "User context — " + "; ".join(parts) + "."
    system = (
        "You are an AI career counselor embedded in the Secure Career System platform. "
        "Help students at every stage — from Class 10 stream choice to PhD research guidance. "
        "Tailor advice to education level, career goal, and interests. "
        "Be concise, helpful, and encouraging. Keep replies under 150 words."
    )
    if context:
        system += f" {context}"
    return _chat(
        [{'role': 'user', 'content': query}],
        system_prompt=system,
        max_tokens=300,
    )
