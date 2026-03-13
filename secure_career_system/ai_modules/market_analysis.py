"""
Global Skill Demand Analysis — returns current and projected market demand
for skills, careers, and industry trends.
"""

from typing import Dict, List

SKILL_DEMAND_DATA: List[Dict] = [
    {
        "skill": "Generative AI / LLMs",
        "demand_score": 98,
        "trend": "Exploding",
        "growth_pct": "+200% YoY",
        "top_domains": ["Technology", "Healthcare", "Finance", "Education"],
        "avg_salary_premium": "30–60% above base",
        "learn_from": ["fast.ai", "Hugging Face Courses", "DeepLearning.AI"],
    },
    {
        "skill": "Machine Learning",
        "demand_score": 95,
        "trend": "Very High",
        "growth_pct": "+40% YoY",
        "top_domains": ["Technology", "Finance", "Research"],
        "avg_salary_premium": "20–45% above base",
        "learn_from": ["Coursera ML Specialization", "Kaggle Learn"],
    },
    {
        "skill": "Cloud Computing (AWS/Azure/GCP)",
        "demand_score": 93,
        "trend": "High",
        "growth_pct": "+35% YoY",
        "top_domains": ["Technology", "Enterprise IT"],
        "avg_salary_premium": "15–35% above base",
        "learn_from": ["AWS Skill Builder", "Google Cloud Skills Boost", "ACloudGuru"],
    },
    {
        "skill": "Cybersecurity",
        "demand_score": 91,
        "trend": "High",
        "growth_pct": "+33% by 2030",
        "top_domains": ["Government", "Finance", "Healthcare", "Technology"],
        "avg_salary_premium": "20–40% above base",
        "learn_from": ["TryHackMe", "CompTIA CertMaster", "Cybrary"],
    },
    {
        "skill": "Data Science / Analytics",
        "demand_score": 90,
        "trend": "High",
        "growth_pct": "+36% by 2030",
        "top_domains": ["Technology", "Finance", "Healthcare", "Retail"],
        "avg_salary_premium": "15–30% above base",
        "learn_from": ["Coursera Data Science", "DataCamp", "Kaggle"],
    },
    {
        "skill": "Python Programming",
        "demand_score": 89,
        "trend": "High",
        "growth_pct": "+28% YoY job postings",
        "top_domains": ["Technology", "Finance", "Science", "Education"],
        "avg_salary_premium": "10–25% above base",
        "learn_from": ["Python.org", "Automate the Boring Stuff", "RealPython"],
    },
    {
        "skill": "Full Stack Development",
        "demand_score": 87,
        "trend": "High",
        "growth_pct": "+25% YoY",
        "top_domains": ["Technology", "Startups"],
        "avg_salary_premium": "10–20% above base",
        "learn_from": ["Full Stack Open", "The Odin Project", "freeCodeCamp"],
    },
    {
        "skill": "DevOps / MLOps",
        "demand_score": 85,
        "trend": "High",
        "growth_pct": "+22% YoY",
        "top_domains": ["Technology", "Enterprise"],
        "avg_salary_premium": "15–30% above base",
        "learn_from": ["Linux Foundation Courses", "Udemy DevOps", "KodeKloud"],
    },
    {
        "skill": "Blockchain / Web3",
        "demand_score": 70,
        "trend": "Moderate",
        "growth_pct": "+12% YoY (volatile)",
        "top_domains": ["Finance", "Technology"],
        "avg_salary_premium": "Variable",
        "learn_from": ["CryptoZombies", "Ethereum.org", "Buildspace"],
    },
    {
        "skill": "UX / Product Design",
        "demand_score": 82,
        "trend": "High",
        "growth_pct": "+13% by 2030",
        "top_domains": ["Technology", "E-commerce", "Fintech"],
        "avg_salary_premium": "10–20% above base",
        "learn_from": ["Google UX Design Certificate", "Interaction Design Foundation"],
    },
    {
        "skill": "Digital Marketing / SEO",
        "demand_score": 78,
        "trend": "Moderate-High",
        "growth_pct": "+10% YoY",
        "top_domains": ["Retail", "Media", "Startups"],
        "avg_salary_premium": "5–15% above base",
        "learn_from": ["Google Digital Garage", "HubSpot Academy"],
    },
    {
        "skill": "Quantum Computing",
        "demand_score": 60,
        "trend": "Emerging",
        "growth_pct": "Early-stage, high future potential",
        "top_domains": ["Research", "Government", "Technology"],
        "avg_salary_premium": "50%+ (specialised)",
        "learn_from": ["IBM Quantum Learning", "Qiskit Textbook"],
    },
]

FASTEST_GROWING_CAREERS: List[Dict] = [
    {"career": "AI / ML Engineer", "growth": "+40% by 2030", "avg_salary": "₹8–40 LPA"},
    {"career": "Data Scientist", "growth": "+36% by 2030", "avg_salary": "₹6–20 LPA"},
    {"career": "Cybersecurity Analyst", "growth": "+33% by 2030", "avg_salary": "₹4–25 LPA"},
    {"career": "Cloud Architect", "growth": "+28% by 2030", "avg_salary": "₹10–40 LPA"},
    {"career": "Healthcare Professional", "growth": "+13% by 2030", "avg_salary": "₹8–60 LPA"},
    {"career": "Financial Analyst", "growth": "+9% by 2030", "avg_salary": "₹4–20 LPA"},
    {"career": "UX Designer", "growth": "+13% by 2030", "avg_salary": "₹4–18 LPA"},
    {"career": "Renewable Energy Engineer", "growth": "+11% by 2030", "avg_salary": "₹5–20 LPA"},
    {"career": "Full Stack Developer", "growth": "+25% by 2028", "avg_salary": "₹4–25 LPA"},
    {"career": "Biotech Researcher", "growth": "+9% by 2030", "avg_salary": "₹5–25 LPA"},
]

DECLINING_INDUSTRIES: List[Dict] = [
    {"industry": "Traditional Print Media", "trend": "-15% by 2030", "alternative": "Digital Content Creation"},
    {"industry": "Manual Data Entry", "trend": "-30% by 2030", "alternative": "Data Analysis / RPA"},
    {"industry": "Routine Customer Support", "trend": "-25% by 2030 (replaced by AI)", "alternative": "AI Operations"},
    {"industry": "Traditional Retail (non-digital)", "trend": "-18% by 2030", "alternative": "E-commerce / Supply Chain"},
    {"industry": "Toll Collection", "trend": "-50% (automation)", "alternative": "Infrastructure Tech"},
    {"industry": "Telemarketing (cold calls)", "trend": "-20% by 2030", "alternative": "Digital Marketing"},
]

INDUSTRY_TRENDS: Dict[str, Dict] = {
    "Technology": {
        "status": "Booming",
        "hot_areas": ["Generative AI", "Cloud Native", "Cybersecurity", "Web3", "Edge Computing"],
        "outlook": "Continued exponential growth through 2030 and beyond",
    },
    "Healthcare": {
        "status": "Stable-Growing",
        "hot_areas": ["Telemedicine", "Health AI", "Medical Devices", "Genomics"],
        "outlook": "Post-COVID boost; AI transforming diagnostics and drug discovery",
    },
    "Finance": {
        "status": "Evolving",
        "hot_areas": ["FinTech", "Algorithmic Trading", "Blockchain", "ESG Finance"],
        "outlook": "Digital transformation displacing traditional banking; FinTech growing fast",
    },
    "Education": {
        "status": "Disrupting",
        "hot_areas": ["EdTech", "AI Tutoring", "Online Certifications", "VR Learning"],
        "outlook": "Traditional institutions supplemented by online learning platforms",
    },
    "Manufacturing": {
        "status": "Automating",
        "hot_areas": ["Industry 4.0", "IoT", "Robotics", "3D Printing"],
        "outlook": "Physical jobs declining; tech roles in manufacturing growing",
    },
    "Renewable Energy": {
        "status": "Booming",
        "hot_areas": ["Solar", "Wind", "Green Hydrogen", "Battery Storage"],
        "outlook": "Government mandates drive massive investment through 2035",
    },
}


def get_skill_demand(top_n: int = 10) -> Dict:
    """Return top in-demand skills ranked by demand score."""
    ranked = sorted(SKILL_DEMAND_DATA, key=lambda x: x["demand_score"], reverse=True)[:top_n]
    return {
        "top_skills": ranked,
        "total_analysed": len(SKILL_DEMAND_DATA),
        "data_note": "Demand scores based on job posting growth, LinkedIn reports, and industry surveys (2024–2025).",
    }


def get_growing_careers(top_n: int = 10) -> Dict:
    """Return fastest-growing career roles."""
    return {
        "fastest_growing": FASTEST_GROWING_CAREERS[:top_n],
        "declining_industries": DECLINING_INDUSTRIES,
    }


def get_full_market_analysis() -> Dict:
    """Return comprehensive global skill demand and market trends."""
    sorted_skills = sorted(SKILL_DEMAND_DATA, key=lambda x: x["demand_score"], reverse=True)
    return {
        "top_skills": sorted_skills,
        "fastest_growing_careers": FASTEST_GROWING_CAREERS,
        "declining_industries": DECLINING_INDUSTRIES,
        "industry_trends": INDUSTRY_TRENDS,
        "summary": {
            "hottest_skill": sorted_skills[0]["skill"] if sorted_skills else "N/A",
            "hottest_career": FASTEST_GROWING_CAREERS[0]["career"] if FASTEST_GROWING_CAREERS else "N/A",
            "most_at_risk": DECLINING_INDUSTRIES[0]["industry"] if DECLINING_INDUSTRIES else "N/A",
        },
    }


def get_skills_for_career(career_name: str) -> List[str]:
    """Return skills most relevant to a specific career based on demand data."""
    career_lower = career_name.lower()
    relevant = []
    for skill_entry in SKILL_DEMAND_DATA:
        domains = [d.lower() for d in skill_entry["top_domains"]]
        if any(career_lower in d for d in domains):
            relevant.append(skill_entry["skill"])
    return relevant
