from secure_career_system.ai_assistant import get_reply, _detect_intents, _detect_career_domain


def test_greeting_reply():
    reply = get_reply("Hello")
    assert "AI Career Assistant" in reply


def test_help_reply():
    reply = get_reply("help")
    assert "Career paths" in reply or "career" in reply.lower()


def test_technology_career_info():
    reply = get_reply("Tell me about tech careers")
    assert "technology" in reply.lower() or "software" in reply.lower()


def test_finance_roles():
    reply = get_reply("What jobs are there in finance?")
    assert "finance" in reply.lower()


def test_healthcare_roadmap():
    reply = get_reply("Show me a healthcare career roadmap")
    assert "healthcare" in reply.lower() or "biology" in reply.lower()


def test_skill_advice():
    reply = get_reply("How do I improve my python skills?")
    assert "python" in reply.lower()


def test_resume_tips():
    reply = get_reply("Give me resume tips")
    assert "resume" in reply.lower()


def test_placement_guidance():
    reply = get_reply("How to prepare for placements?")
    assert "placement" in reply.lower() or "cgpa" in reply.lower()


def test_mentor_guidance():
    reply = get_reply("How do I find a mentor?")
    assert "mentor" in reply.lower()


def test_empty_query():
    reply = get_reply("")
    assert "AI Career Assistant" in reply


def test_thanks_reply():
    reply = get_reply("Thank you!")
    assert "welcome" in reply.lower()


def test_user_skills_context():
    reply = get_reply("What should I do?", user_skills=["python", "sql", "react"])
    assert "python" in reply.lower() or "skills" in reply.lower()


def test_detect_intents():
    intents = _detect_intents("Tell me about career paths")
    assert "career_info" in intents


def test_detect_career_domain_tech():
    domain = _detect_career_domain("I want a software developer career")
    assert domain == "technology"


def test_detect_career_domain_finance():
    domain = _detect_career_domain("Tell me about banking careers")
    assert domain == "finance"


def test_detect_career_domain_healthcare():
    domain = _detect_career_domain("I want to be a doctor")
    assert domain == "healthcare"


def test_course_recommendation():
    reply = get_reply("Recommend courses for technology")
    assert "course" in reply.lower() or "coursera" in reply.lower()


def test_fallback_reply():
    reply = get_reply("xyzabc random gibberish 12345")
    assert "AI Career Assistant" in reply
