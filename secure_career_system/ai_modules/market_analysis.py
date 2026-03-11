"""
Global Skill Demand Analysis — returns data on top skills in demand,
fastest growing careers, and declining industries.
"""

SKILL_DEMAND_DATA = {
    'top_skills': [
        {'skill': 'Artificial Intelligence / Machine Learning', 'demand_level': 'Very High',
         'growth_rate': '+35%', 'avg_salary': '₹8-25 LPA',
         'industries': ['Technology', 'Finance', 'Healthcare']},
        {'skill': 'Cybersecurity', 'demand_level': 'Very High',
         'growth_rate': '+32%', 'avg_salary': '₹6-20 LPA',
         'industries': ['Technology', 'Banking', 'Government']},
        {'skill': 'Cloud Computing (AWS/Azure/GCP)', 'demand_level': 'Very High',
         'growth_rate': '+28%', 'avg_salary': '₹7-22 LPA',
         'industries': ['Technology', 'E-commerce', 'Healthcare']},
        {'skill': 'Data Science & Analytics', 'demand_level': 'High',
         'growth_rate': '+25%', 'avg_salary': '₹6-20 LPA',
         'industries': ['Technology', 'Finance', 'Retail']},
        {'skill': 'Full Stack Development', 'demand_level': 'High',
         'growth_rate': '+22%', 'avg_salary': '₹5-18 LPA',
         'industries': ['Technology', 'Startups', 'E-commerce']},
        {'skill': 'DevOps & CI/CD', 'demand_level': 'High',
         'growth_rate': '+20%', 'avg_salary': '₹6-18 LPA',
         'industries': ['Technology', 'Finance', 'Telecom']},
        {'skill': 'Blockchain Development', 'demand_level': 'Medium-High',
         'growth_rate': '+18%', 'avg_salary': '₹8-25 LPA',
         'industries': ['Finance', 'Technology', 'Supply Chain']},
        {'skill': 'UI/UX Design', 'demand_level': 'High',
         'growth_rate': '+18%', 'avg_salary': '₹4-15 LPA',
         'industries': ['Technology', 'E-commerce', 'Media']},
        {'skill': 'Digital Marketing & SEO', 'demand_level': 'High',
         'growth_rate': '+15%', 'avg_salary': '₹3-12 LPA',
         'industries': ['E-commerce', 'Media', 'Startups']},
        {'skill': 'Generative AI & Prompt Engineering', 'demand_level': 'Very High',
         'growth_rate': '+40%', 'avg_salary': '₹8-30 LPA',
         'industries': ['Technology', 'Creative', 'Education']},
    ],
    'fastest_growing_careers': [
        {'career': 'AI/ML Engineer', 'growth': '+35%', 'entry_salary': '₹6-12 LPA'},
        {'career': 'Cloud Solutions Architect', 'growth': '+28%', 'entry_salary': '₹8-15 LPA'},
        {'career': 'Cybersecurity Analyst', 'growth': '+32%', 'entry_salary': '₹5-10 LPA'},
        {'career': 'Data Engineer', 'growth': '+25%', 'entry_salary': '₹6-12 LPA'},
        {'career': 'Full Stack Developer', 'growth': '+22%', 'entry_salary': '₹4-10 LPA'},
        {'career': 'DevOps Engineer', 'growth': '+20%', 'entry_salary': '₹5-12 LPA'},
        {'career': 'Product Manager', 'growth': '+18%', 'entry_salary': '₹8-15 LPA'},
        {'career': 'Blockchain Developer', 'growth': '+18%', 'entry_salary': '₹6-15 LPA'},
    ],
    'declining_industries': [
        {'industry': 'Traditional Manufacturing (manual)', 'trend': 'Declining',
         'reason': 'Automation and robotics replacing manual labor'},
        {'industry': 'Print Media', 'trend': 'Declining',
         'reason': 'Digital media and online content consumption growing'},
        {'industry': 'Basic Data Entry', 'trend': 'Declining',
         'reason': 'AI and automation replacing repetitive tasks'},
        {'industry': 'Traditional Retail (non-digital)', 'trend': 'Declining',
         'reason': 'E-commerce and digital-first shopping experiences'},
    ],
}


def get_skill_demand():
    """Return current skill demand analysis data."""
    return SKILL_DEMAND_DATA


def get_top_skills(limit=10):
    """Return top N skills in demand."""
    return SKILL_DEMAND_DATA['top_skills'][:limit]


def get_growing_careers(limit=8):
    """Return fastest growing careers."""
    return SKILL_DEMAND_DATA['fastest_growing_careers'][:limit]


def get_declining_industries():
    """Return declining industries."""
    return SKILL_DEMAND_DATA['declining_industries']
