import pytest
from backend.models.student import (
    StudentProfile,
    Education,
    SkillItem,
    SkillProficiency,
    SkillCategory,
    CareerGoal,
    Project,
)
from backend.models.dossier import (
    SkillGapItem,
    GapStatus,
    GapSeverity,
    SkillGapReport,
)

def test_student_profile_creation():
    edu = Education(
        institution="Stanford University",
        degree="B.S.",
        major="Computer Science",
        graduation_year=2026,
        gpa="3.9/4.0",
        coursework=["CS 229: Machine Learning", "CS 106B: Programming Abstractions"]
    )
    goal = CareerGoal(
        target_role="Junior Machine Learning Engineer",
        seniority_level="Entry-Level",
        timeline_months=6
    )
    skills = [
        SkillItem(name="Python", proficiency=SkillProficiency.ADVANCED, category=SkillCategory.PROGRAMMING),
        SkillItem(name="PyTorch", proficiency=SkillProficiency.INTERMEDIATE, category=SkillCategory.DATA_ML)
    ]
    projects = [
        Project(
            title="Transformer NLP",
            description="Built a sentiment analysis transformer.",
            tech_stack=["Python", "PyTorch"],
            highlights=["92% F1 score"]
        )
    ]

    profile = StudentProfile(
        name="Taylor Swift",
        email="taylor@cs.stanford.edu",
        education=edu,
        skills=skills,
        career_goal=goal,
        projects=projects,
        hours_per_week_available=15
    )

    assert profile.name == "Taylor Swift"
    assert len(profile.skills) == 2
    assert profile.skills[0].proficiency == SkillProficiency.ADVANCED
    assert profile.hours_per_week_available == 15

def test_skill_gap_item_creation():
    item = SkillGapItem(
        skill_name="Docker Containers",
        category="Developer Tools & CI/CD",
        status=GapStatus.MISSING,
        required_proficiency="intermediate",
        severity=GapSeverity.HIGH,
        importance_weight=2.0,
        impact_analysis="Essential for containerized deployments.",
        remediation_priority=2
    )
    assert item.status == GapStatus.MISSING
    assert item.severity == GapSeverity.HIGH
    assert item.current_proficiency is None
