"""
Career Opportunity Map — provides a comprehensive map of a career including
required skills, average salary, demand level, and growth trajectory.
"""

CAREER_MAP_DATABASE = {
    'Data Scientist': {
        'required_skills': ['Python', 'Machine Learning', 'Statistics', 'SQL', 'Data Visualization',
                            'Deep Learning', 'Pandas', 'TensorFlow/PyTorch'],
        'average_salary': '₹6-20 LPA',
        'demand_level': 'High',
        'growth_trajectory': 'Data Analyst → Data Scientist → Senior Data Scientist → Lead/Principal → Chief Data Officer',
        'top_companies': ['Google', 'Microsoft', 'Amazon', 'Flipkart', 'Swiggy'],
        'certifications': ['Google Data Analytics', 'IBM Data Science Professional', 'AWS ML Specialty'],
    },
    'Software Engineer': {
        'required_skills': ['Python/Java/C++', 'Data Structures', 'Algorithms', 'System Design',
                            'Git', 'SQL', 'REST APIs', 'Testing'],
        'average_salary': '₹5-25 LPA',
        'demand_level': 'Very High',
        'growth_trajectory': 'Junior Developer → Software Engineer → Senior Engineer → Staff Engineer → Principal Engineer',
        'top_companies': ['Google', 'Microsoft', 'Amazon', 'Flipkart', 'Infosys'],
        'certifications': ['AWS Developer Associate', 'Google Associate Cloud Engineer'],
    },
    'AI/ML Engineer': {
        'required_skills': ['Python', 'Machine Learning', 'Deep Learning', 'TensorFlow/PyTorch',
                            'NLP', 'Computer Vision', 'MLOps', 'Mathematics'],
        'average_salary': '₹8-30 LPA',
        'demand_level': 'Very High',
        'growth_trajectory': 'ML Intern → ML Engineer → Senior ML Engineer → AI Architect → VP of AI',
        'top_companies': ['Google', 'OpenAI', 'Microsoft', 'NVIDIA', 'Amazon'],
        'certifications': ['TensorFlow Developer Certificate', 'AWS ML Specialty', 'Google ML Engineer'],
    },
    'Cybersecurity Analyst': {
        'required_skills': ['Networking', 'Linux', 'Security Tools', 'Python', 'Penetration Testing',
                            'SIEM', 'Incident Response', 'Cryptography'],
        'average_salary': '₹6-20 LPA',
        'demand_level': 'Very High',
        'growth_trajectory': 'SOC Analyst → Security Analyst → Security Engineer → Security Architect → CISO',
        'top_companies': ['Deloitte', 'PwC', 'IBM', 'Cisco', 'Palo Alto Networks'],
        'certifications': ['CompTIA Security+', 'CEH', 'CISSP', 'OSCP'],
    },
    'Cloud Architect': {
        'required_skills': ['AWS/Azure/GCP', 'Docker', 'Kubernetes', 'Terraform', 'Networking',
                            'Linux', 'CI/CD', 'Python'],
        'average_salary': '₹10-35 LPA',
        'demand_level': 'Very High',
        'growth_trajectory': 'Cloud Support → Cloud Engineer → Solutions Architect → Principal Architect',
        'top_companies': ['AWS', 'Microsoft', 'Google', 'IBM', 'Oracle'],
        'certifications': ['AWS Solutions Architect', 'Azure Solutions Architect', 'GCP Professional'],
    },
    'Financial Analyst': {
        'required_skills': ['Excel', 'Financial Modeling', 'SQL', 'Data Analysis', 'Accounting',
                            'Power BI/Tableau', 'Statistics'],
        'average_salary': '₹4-15 LPA',
        'demand_level': 'High',
        'growth_trajectory': 'Analyst → Senior Analyst → Manager → Director → CFO',
        'top_companies': ['Goldman Sachs', 'JP Morgan', 'HDFC', 'ICICI', 'Deloitte'],
        'certifications': ['CFA', 'CPA', 'FRM'],
    },
    'Product Manager': {
        'required_skills': ['Product Strategy', 'Data Analysis', 'SQL', 'Communication',
                            'Agile/Scrum', 'User Research', 'Wireframing'],
        'average_salary': '₹8-25 LPA',
        'demand_level': 'High',
        'growth_trajectory': 'APM → Product Manager → Senior PM → Director of Product → VP of Product → CPO',
        'top_companies': ['Google', 'Microsoft', 'Amazon', 'Flipkart', 'Razorpay'],
        'certifications': ['Certified Scrum Product Owner', 'PMI-ACP'],
    },
    'UX Designer': {
        'required_skills': ['Figma', 'User Research', 'Prototyping', 'Wireframing',
                            'Visual Design', 'HTML/CSS', 'Design Thinking'],
        'average_salary': '₹4-18 LPA',
        'demand_level': 'High',
        'growth_trajectory': 'Junior Designer → UX Designer → Senior UX → Lead Designer → Head of Design',
        'top_companies': ['Google', 'Apple', 'Microsoft', 'Swiggy', 'Razorpay'],
        'certifications': ['Google UX Design Certificate', 'Interaction Design Foundation'],
    },
    'Full Stack Developer': {
        'required_skills': ['JavaScript', 'React/Angular/Vue', 'Node.js', 'SQL/NoSQL',
                            'HTML/CSS', 'Git', 'REST APIs', 'Docker'],
        'average_salary': '₹5-20 LPA',
        'demand_level': 'High',
        'growth_trajectory': 'Junior Developer → Developer → Senior Developer → Tech Lead → CTO',
        'top_companies': ['Google', 'Amazon', 'Flipkart', 'Zomato', 'Paytm'],
        'certifications': ['Meta Front-End Developer', 'AWS Developer Associate'],
    },
    'Doctor (MBBS)': {
        'required_skills': ['Biology', 'Chemistry', 'Patient Care', 'Clinical Skills',
                            'Communication', 'Research Methodology'],
        'average_salary': '₹6-25 LPA',
        'demand_level': 'High',
        'growth_trajectory': 'MBBS → Internship → MD/MS Residency → Senior Consultant → HOD',
        'top_companies': ['AIIMS', 'Apollo Hospitals', 'Fortis', 'Max Healthcare', 'Medanta'],
        'certifications': ['NEET PG', 'USMLE (for abroad)'],
    },
}


def get_career_map(career):
    """Get the career opportunity map for a specific career.

    Returns career details including required skills, salary, demand, etc.
    """
    # Exact match
    if career in CAREER_MAP_DATABASE:
        data = CAREER_MAP_DATABASE[career]
        return {'career': career, **data}

    # Partial match
    career_lower = career.lower()
    for name, data in CAREER_MAP_DATABASE.items():
        if career_lower in name.lower() or name.lower() in career_lower:
            return {'career': name, **data}

    return {
        'career': career,
        'message': 'Career map not found for this career. Try a more common career title.',
        'available_careers': list(CAREER_MAP_DATABASE.keys()),
    }


def list_all_careers():
    """Return all available careers in the map."""
    return list(CAREER_MAP_DATABASE.keys())
