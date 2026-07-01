"""Tests for the AI skill gap analyzer module."""
from secure_career_system.skill_gap_analyzer import analyze_skill_gap


def test_full_match():
    """When a user has all required skills the match percentage should be 100."""
    result = analyze_skill_gap(
        ['python', 'java', 'c++', 'sql', 'git', 'data structures',
         'algorithms', 'machine learning', 'docker', 'aws', 'react',
         'node', 'linux', 'agile'],
        'Technology',
    )
    assert result['match_percentage'] == 100.0
    assert result['missing_skills'] == []
    assert len(result['matched_skills']) == 14


def test_partial_match():
    result = analyze_skill_gap(['python', 'sql'], 'Technology')
    assert 0 < result['match_percentage'] < 100
    assert 'python' in result['matched_skills']
    assert 'sql' in result['matched_skills']
    assert len(result['missing_skills']) > 0


def test_no_match():
    result = analyze_skill_gap(['cooking'], 'Technology')
    assert result['match_percentage'] == 0.0
    assert len(result['missing_skills']) == 14


def test_missing_sorted_by_importance():
    result = analyze_skill_gap([], 'Technology')
    importances = [result['recommendations'][s]['importance'] for s in result['missing_skills']]
    # Should be descending
    assert importances == sorted(importances, reverse=True)


def test_career_case_insensitive():
    result = analyze_skill_gap(['python'], 'technology')
    assert result['career'] == 'Technology'


def test_unknown_career_returns_empty():
    result = analyze_skill_gap(['python'], 'Unknown')
    assert result['matched_skills'] == []
    assert result['missing_skills'] == []


def test_finance_career():
    result = analyze_skill_gap(['excel', 'sql', 'communication'], 'Finance')
    assert 'excel' in result['matched_skills']
    assert result['match_percentage'] > 0


def test_healthcare_career():
    result = analyze_skill_gap(['biology', 'chemistry'], 'Healthcare')
    assert 'biology' in result['matched_skills']
    assert 'chemistry' in result['matched_skills']
