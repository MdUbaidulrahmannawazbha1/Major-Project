"""
Career Opportunity Map — returns detailed career profiles including
required skills, salary range, demand level, and growth trajectory.
"""

from typing import Dict, List, Optional

CAREER_MAP: Dict[str, Dict] = {
    "Data Scientist": {
        "domain": "Technology",
        "description": "Extracts insights from complex data using statistical models and machine learning.",
        "required_skills": [
            "Python", "Machine Learning", "Statistics", "SQL",
            "Data Visualization", "Deep Learning", "Communication",
        ],
        "nice_to_have": ["Spark", "Hadoop", "Cloud Platforms", "NLP"],
        "education": ["B.Sc Statistics", "B.Tech CS", "M.Sc Data Science", "MBA Analytics"],
        "certifications": [
            "Google Professional ML Engineer",
            "AWS Certified ML Specialist",
            "IBM Data Science Professional Certificate",
        ],
        "average_salary": "₹6–20 LPA",
        "demand_level": "Very High",
        "growth_rate": "+36% by 2030 (US BLS)",
        "top_companies": ["Google", "Amazon", "Microsoft", "Flipkart", "Fractal Analytics"],
        "career_progression": [
            "Data Analyst → Junior Data Scientist → Data Scientist → Senior Data Scientist → Principal DS → CDO"
        ],
    },
    "Software Engineer": {
        "domain": "Technology",
        "description": "Designs, develops, and maintains software systems and applications.",
        "required_skills": [
            "Programming (Python/Java/C++)", "Data Structures", "Algorithms",
            "System Design", "Git", "SQL", "Testing",
        ],
        "nice_to_have": ["Cloud (AWS/GCP)", "Docker", "Kubernetes", "CI/CD"],
        "education": ["B.Tech CS", "BCA", "B.Sc Computer Science"],
        "certifications": [
            "AWS Solutions Architect",
            "Google Cloud Professional",
            "Oracle Java SE Certified Developer",
        ],
        "average_salary": "₹4–35 LPA",
        "demand_level": "High",
        "growth_rate": "+25% by 2030",
        "top_companies": ["Google", "Microsoft", "Amazon", "Infosys", "TCS", "Startups"],
        "career_progression": [
            "Junior Dev → Software Engineer → Senior Engineer → Tech Lead → Engineering Manager → CTO"
        ],
    },
    "AI Engineer": {
        "domain": "Technology",
        "description": "Builds AI-powered systems including NLP, computer vision, and generative AI applications.",
        "required_skills": [
            "Python", "TensorFlow/PyTorch", "Machine Learning",
            "Deep Learning", "MLOps", "Cloud Platforms", "Mathematics",
        ],
        "nice_to_have": ["LLMs", "RAG Systems", "CUDA", "Research writing"],
        "education": ["B.Tech CS/AI", "M.Tech AI", "M.Sc AI"],
        "certifications": [
            "TensorFlow Developer Certificate",
            "AWS ML Specialty",
            "NVIDIA Deep Learning Institute",
        ],
        "average_salary": "₹8–40 LPA",
        "demand_level": "Very High",
        "growth_rate": "+40% by 2030",
        "top_companies": ["OpenAI", "Google DeepMind", "Microsoft AI", "Anthropic", "Startups"],
        "career_progression": [
            "ML Engineer → AI Engineer → Senior AI Engineer → AI Architect → AI Research Lead"
        ],
    },
    "Cybersecurity Analyst": {
        "domain": "Technology",
        "description": "Protects systems from cyber threats through monitoring, analysis, and response.",
        "required_skills": [
            "Network Security", "SIEM Tools", "Penetration Testing",
            "Python/Bash Scripting", "Incident Response", "Compliance",
        ],
        "nice_to_have": ["Malware Analysis", "Digital Forensics", "Cloud Security"],
        "education": ["B.Tech CS", "B.Sc IT", "Information Security programmes"],
        "certifications": [
            "CEH (Certified Ethical Hacker)",
            "CISSP",
            "CompTIA Security+",
            "OSCP",
        ],
        "average_salary": "₹4–25 LPA",
        "demand_level": "High",
        "growth_rate": "+33% by 2030 (US BLS)",
        "top_companies": ["Palo Alto Networks", "CrowdStrike", "IBM Security", "TCS Cyber"],
        "career_progression": [
            "SOC Analyst → Security Analyst → Senior Analyst → Security Architect → CISO"
        ],
    },
    "Financial Analyst": {
        "domain": "Finance",
        "description": "Analyses financial data to guide investment and business decisions.",
        "required_skills": [
            "Financial Modelling", "Excel", "Valuation", "Accounting",
            "Python/R for data", "Communication", "CFA knowledge",
        ],
        "nice_to_have": ["Bloomberg Terminal", "Power BI", "SQL"],
        "education": ["B.Com", "BBA Finance", "MBA Finance", "CA"],
        "certifications": ["CFA Level 1/2/3", "CA (ICAI)", "FRM", "CPA"],
        "average_salary": "₹4–20 LPA",
        "demand_level": "High",
        "growth_rate": "+9% by 2030",
        "top_companies": ["Goldman Sachs", "JP Morgan", "HDFC Bank", "Deloitte", "KPMG"],
        "career_progression": [
            "Junior Analyst → Financial Analyst → Senior Analyst → VP Finance → CFO"
        ],
    },
    "Doctor": {
        "domain": "Healthcare",
        "description": "Diagnoses and treats medical conditions; provides patient care.",
        "required_skills": [
            "Clinical Knowledge", "Patient Communication", "Diagnosis",
            "Anatomy & Physiology", "Pharmacology", "Emergency Care",
        ],
        "nice_to_have": ["Research Skills", "AI in Medicine", "Telemedicine"],
        "education": ["MBBS + PG (MD/MS)", "BDS", "BAMS"],
        "certifications": [
            "NBE Board Certification",
            "MCI Registration",
            "Fellowship (specialty-specific)",
        ],
        "average_salary": "₹8–60 LPA",
        "demand_level": "Very High",
        "growth_rate": "+13% by 2030 (global)",
        "top_companies": ["AIIMS", "Apollo Hospitals", "Fortis", "Medanta"],
        "career_progression": [
            "Intern → Resident → Junior Doctor → Consultant → Senior Consultant → HOD"
        ],
    },
    "Lawyer": {
        "domain": "Arts",
        "description": "Advises clients on legal matters, drafts documents, and represents them in court.",
        "required_skills": [
            "Legal Research", "Advocacy", "Drafting", "Critical Thinking",
            "Negotiation", "Communication",
        ],
        "nice_to_have": ["Alternative Dispute Resolution", "Legal Tech", "International Law"],
        "education": ["LLB", "BA LLB (5-year integrated)", "LLM for specialization"],
        "certifications": [
            "Bar Council Enrollment",
            "Cyberlaw Certificate",
            "LLM in specific domain",
        ],
        "average_salary": "₹4–30 LPA",
        "demand_level": "Moderate",
        "growth_rate": "+8% by 2030",
        "top_companies": ["AZB & Partners", "Cyril Amarchand Mangaldas", "J. Sagar Associates"],
        "career_progression": [
            "Associate → Junior Lawyer → Senior Associate → Partner → Managing Partner"
        ],
    },
    "Civil Servant (IAS)": {
        "domain": "Government",
        "description": "Administers government policy and public services across India.",
        "required_skills": [
            "General Studies (History, Polity, Economy)",
            "Analytical Writing", "Decision Making",
            "Leadership", "Crisis Management",
        ],
        "nice_to_have": ["Optional Subject Expertise", "Regional Languages"],
        "education": ["Any Graduation"],
        "certifications": ["UPSC CSE Rank"],
        "average_salary": "₹6–20 LPA (Government Pay Scale) + Perks",
        "demand_level": "Competitive",
        "growth_rate": "Steady government opportunity",
        "top_companies": ["Government of India", "State Governments", "IAS posts"],
        "career_progression": [
            "IAS Probationer → SDM → DM/Collector → Secretary → Chief Secretary"
        ],
    },
    "UX Designer": {
        "domain": "Design",
        "description": "Designs user-centred digital interfaces and experiences.",
        "required_skills": [
            "Figma / Adobe XD", "User Research", "Wireframing",
            "Prototyping", "Interaction Design", "Usability Testing",
        ],
        "nice_to_have": ["HTML/CSS", "Motion Design", "Design Systems"],
        "education": ["B.Des", "B.Tech CS", "Any graduation + UX bootcamp"],
        "certifications": [
            "Google UX Design Professional Certificate",
            "Interaction Design Foundation",
        ],
        "average_salary": "₹4–18 LPA",
        "demand_level": "High",
        "growth_rate": "+13% by 2030",
        "top_companies": ["Google", "Apple", "Flipkart", "Design studios", "Startups"],
        "career_progression": [
            "UX Researcher → UX Designer → Senior UX → Lead Designer → Design Director"
        ],
    },
    "Research Scientist": {
        "domain": "Research",
        "description": "Conducts original research to advance knowledge in a scientific domain.",
        "required_skills": [
            "Research Methodology", "Academic Writing", "Data Analysis",
            "Python / MATLAB / R", "Publications", "Domain Expertise",
        ],
        "nice_to_have": ["Grant Writing", "Collaboration", "Teaching"],
        "education": ["PhD in relevant field", "M.Sc / M.Tech as stepping stone"],
        "certifications": [
            "CSIR NET (India)",
            "UGC NET",
            "Postdoctoral fellowship",
        ],
        "average_salary": "₹5–25 LPA (academia) / ₹15–50 LPA (industry research)",
        "demand_level": "Moderate-High",
        "growth_rate": "+9% by 2030",
        "top_companies": ["IITs", "IISc", "DRDO", "ISRO", "Google Research", "Microsoft Research"],
        "career_progression": [
            "Research Assistant → Junior Researcher → Scientist → Senior Scientist → Fellow"
        ],
    },
}


def get_career_map(career_name: str) -> Optional[Dict]:
    """
    Return the career opportunity map for a specific career.

    Args:
        career_name: Name of the career (partial match supported).

    Returns:
        dict with career profile or None if not found.
    """
    # Exact match first
    if career_name in CAREER_MAP:
        return {"career": career_name, **CAREER_MAP[career_name]}

    # Case-insensitive partial match
    career_lower = career_name.lower()
    for key, info in CAREER_MAP.items():
        if career_lower in key.lower() or key.lower() in career_lower:
            return {"career": key, **info}

    return None


def get_all_careers() -> List[Dict]:
    """Return all career entries."""
    return [{"career": name, **info} for name, info in CAREER_MAP.items()]


def get_careers_by_domain(domain: str) -> List[Dict]:
    """Return careers filtered by domain."""
    return [
        {"career": name, **info}
        for name, info in CAREER_MAP.items()
        if info["domain"].lower() == domain.lower()
    ]
