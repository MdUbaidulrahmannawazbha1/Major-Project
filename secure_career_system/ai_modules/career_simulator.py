"""
Career Simulator — generates a step-by-step career path from the user's
current position to their target career goal.
"""

from typing import Dict, List, Optional

# Predefined simulation paths for common career trajectories
SIMULATION_PATHS: Dict[str, List[Dict]] = {
    "AI Engineer": [
        {"step": 1, "title": "Choose Science Stream (Class 11-12)", "action": "Focus on PCM + Computer Science", "duration": "2 years"},
        {"step": 2, "title": "Pursue B.Tech Computer Science", "action": "Target IIT/NIT/IIIT via JEE; or BCA/B.Sc CS as alternate", "duration": "4 years"},
        {"step": 3, "title": "Learn Python & Mathematics", "action": "Complete Python for Everybody (Coursera) + Statistics basics", "duration": "3 months"},
        {"step": 4, "title": "Master Machine Learning", "action": "Andrew Ng ML Course on Coursera; implement 3 ML projects", "duration": "4 months"},
        {"step": 5, "title": "Specialize in Deep Learning / LLMs", "action": "TensorFlow / PyTorch; explore NLP, Computer Vision, Generative AI", "duration": "4 months"},
        {"step": 6, "title": "Build AI Portfolio", "action": "3 GitHub projects: chatbot, image classifier, recommendation system", "duration": "2 months"},
        {"step": 7, "title": "Internship", "action": "Apply for ML/AI internship at tech startup or Big Tech", "duration": "6 months"},
        {"step": 8, "title": "Full-time AI Engineer Role", "action": "Apply at AI-first companies; target ₹8–25 LPA fresher salary", "duration": "Ongoing"},
    ],
    "Data Scientist": [
        {"step": 1, "title": "Build Programming Foundation", "action": "Learn Python + SQL basics", "duration": "2 months"},
        {"step": 2, "title": "Learn Statistics & Mathematics", "action": "Probability, Linear Algebra, Hypothesis Testing", "duration": "2 months"},
        {"step": 3, "title": "Core Data Science Skills", "action": "pandas, numpy, matplotlib, scikit-learn", "duration": "3 months"},
        {"step": 4, "title": "Machine Learning Projects", "action": "Kaggle competitions; 3 end-to-end projects", "duration": "3 months"},
        {"step": 5, "title": "Internship or Analyst Role", "action": "Data Analyst or Junior DS internship", "duration": "6 months"},
        {"step": 6, "title": "Become Data Scientist", "action": "Full-time DS role; ₹6–15 LPA starting salary", "duration": "Ongoing"},
    ],
    "Doctor": [
        {"step": 1, "title": "Science Stream (PCB)", "action": "Focus on Physics, Chemistry, Biology in Class 11-12", "duration": "2 years"},
        {"step": 2, "title": "NEET Preparation", "action": "Enroll at Aakash/Allen; target 650+ score in NEET", "duration": "1-2 years"},
        {"step": 3, "title": "MBBS", "action": "Pursue MBBS at Government Medical College (5.5 years)", "duration": "5.5 years"},
        {"step": 4, "title": "Internship", "action": "Mandatory 1-year rotatory internship", "duration": "1 year"},
        {"step": 5, "title": "Postgraduate (MD/MS)", "action": "NEET-PG preparation for specialization", "duration": "3 years"},
        {"step": 6, "title": "Established Doctor", "action": "Practice as Specialist; ₹15–60 LPA potential", "duration": "Ongoing"},
    ],
    "Software Engineer": [
        {"step": 1, "title": "Programming Foundation", "action": "Learn any language: Python, Java, or C++", "duration": "3 months"},
        {"step": 2, "title": "Data Structures & Algorithms", "action": "Complete 150 LeetCode problems", "duration": "4 months"},
        {"step": 3, "title": "Build Projects", "action": "2 full-stack or system projects on GitHub", "duration": "3 months"},
        {"step": 4, "title": "Open Source Contribution", "action": "Contribute to 2 open-source projects", "duration": "2 months"},
        {"step": 5, "title": "Internship / Campus Placement", "action": "Apply via campus or internship portals", "duration": "6 months"},
        {"step": 6, "title": "Software Engineer", "action": "Full-time role; ₹4–20 LPA fresher salary", "duration": "Ongoing"},
    ],
    "IAS Officer": [
        {"step": 1, "title": "Choose Any Stream", "action": "Focus on Current Affairs, History, Polity from Class 11", "duration": "2 years"},
        {"step": 2, "title": "Graduation", "action": "Any bachelor's degree (optional subject selection matters)", "duration": "3-4 years"},
        {"step": 3, "title": "UPSC CSE Preparation", "action": "Enroll at Vision IAS / Vajiram; 18 months dedicated prep", "duration": "18 months"},
        {"step": 4, "title": "Clear UPSC Prelims", "action": "GS Paper I + CSAT; shortlisting for Mains", "duration": "6 months"},
        {"step": 5, "title": "Clear UPSC Mains", "action": "9 papers including Optional; Essay; GS I-IV", "duration": "6 months"},
        {"step": 6, "title": "Personality Interview", "action": "Board interview; Dossier preparation", "duration": "3 months"},
        {"step": 7, "title": "IAS Officer", "action": "LBSNAA training + Posting as Probationary IAS", "duration": "Ongoing"},
    ],
    "Lawyer": [
        {"step": 1, "title": "Arts / Commerce Stream", "action": "Focus on Language, Political Science, Economics", "duration": "2 years"},
        {"step": 2, "title": "CLAT Preparation", "action": "Legal reasoning, GK, English, Logical Reasoning", "duration": "1 year"},
        {"step": 3, "title": "BA LLB (5 years)", "action": "Enroll at NLU or top law college; internships each summer", "duration": "5 years"},
        {"step": 4, "title": "Bar Council Enrollment", "action": "Register with State Bar Council", "duration": "1 month"},
        {"step": 5, "title": "Junior Associate", "action": "Join law firm or High Court chamber", "duration": "2-3 years"},
        {"step": 6, "title": "Established Lawyer", "action": "Senior Associate / Partner track; ₹8–30 LPA potential", "duration": "Ongoing"},
    ],
    "UX Designer": [
        {"step": 1, "title": "Learn Design Basics", "action": "Color theory, typography, Figma basics", "duration": "2 months"},
        {"step": 2, "title": "UX Fundamentals", "action": "User Research, Wireframing, Prototyping", "duration": "2 months"},
        {"step": 3, "title": "Google UX Design Certificate", "action": "Complete 6-month Coursera program", "duration": "6 months"},
        {"step": 4, "title": "Build Portfolio", "action": "3 UX case studies (problem → research → design → test)", "duration": "3 months"},
        {"step": 5, "title": "Internship", "action": "Junior UX Designer internship at product company", "duration": "6 months"},
        {"step": 6, "title": "UX Designer", "action": "Full-time role; ₹4–15 LPA starting", "duration": "Ongoing"},
    ],
}


def simulate_career(
    target_career: str,
    education_level: str,
    current_skills: Optional[List[str]] = None,
    starting_point: Optional[str] = None,
) -> Dict:
    """
    Generate a step-by-step career simulation from current position to target.

    Args:
        target_career: Desired career destination.
        education_level: Current education level.
        current_skills: Skills already possessed.
        starting_point: Current role or stage (e.g., 'school student', 'engineer').

    Returns:
        dict containing the step-by-step simulation path.
    """
    current_skills = current_skills or []

    # Find best matching path
    path = None
    target_lower = target_career.lower()
    for key, steps in SIMULATION_PATHS.items():
        if key.lower() in target_lower or target_lower in key.lower():
            path = steps
            break

    if path is None:
        # Generic path
        path = [
            {"step": 1, "title": "Foundation Learning", "action": f"Learn the fundamentals required for {target_career}", "duration": "3 months"},
            {"step": 2, "title": "Skill Development", "action": "Build core technical and soft skills for the domain", "duration": "6 months"},
            {"step": 3, "title": "Projects & Portfolio", "action": f"Build 2-3 real projects relevant to {target_career}", "duration": "3 months"},
            {"step": 4, "title": "Networking & Internship", "action": "Connect with professionals and seek internship / entry role", "duration": "3 months"},
            {"step": 5, "title": f"Become {target_career}", "action": "Apply for full-time positions and advance your career", "duration": "Ongoing"},
        ]

    # Accelerate path based on education level and existing skills
    step_offset = 0
    if education_level in ["Undergraduate", "Postgraduate", "PhD", "Professional"]:
        step_offset = 1  # Skip the very first school step if applicable
    if len(current_skills) >= 5:
        step_offset = min(step_offset + 1, 2)

    adjusted_path = path[step_offset:] if step_offset < len(path) else path

    # Recalculate step numbers
    for i, step in enumerate(adjusted_path):
        step = dict(step)
        step["step"] = i + 1
        adjusted_path[i] = step

    total_steps = len(adjusted_path)
    estimated_duration = _estimate_total_duration(adjusted_path)

    return {
        "target_career": target_career,
        "education_level": education_level,
        "current_skills": current_skills,
        "starting_step": step_offset + 1,
        "total_steps": total_steps,
        "estimated_duration": estimated_duration,
        "simulation_path": adjusted_path,
        "message": f"Your personalised path to becoming a {target_career} has {total_steps} steps.",
    }


def _estimate_total_duration(path: List[Dict]) -> str:
    """Estimate total duration in months from path steps."""
    total_months = 0
    for step in path:
        dur = step.get("duration", "")
        if "ongoing" in dur.lower():
            total_months += 12  # treat ongoing as +1 year for a realistic estimate
        elif "year" in dur:
            try:
                y = float(dur.split()[0])
                total_months += int(y * 12)
            except (ValueError, IndexError):
                total_months += 12
        elif "month" in dur:
            try:
                parts = dur.split()[0]
                if "-" in parts:
                    low, high = parts.split("-")
                    total_months += (int(low) + int(high)) // 2
                else:
                    total_months += int(parts)
            except (ValueError, IndexError):
                total_months += 3
    if total_months == 0:
        return "Variable"
    if total_months >= 12:
        years = total_months // 12
        months = total_months % 12
        return f"{years} year{'s' if years > 1 else ''}" + (f" {months} months" if months else "")
    return f"{total_months} months"
