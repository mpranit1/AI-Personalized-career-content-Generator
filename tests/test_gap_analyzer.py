import pytest
from backend.models.student import (
    StudentProfile,
    Education,
    SkillItem,
    SkillProficiency,
    SkillCategory,
    CareerGoal,
)
from backend.models.career_data import ROLE_BENCHMARKS
from backend.services.gap_analyzer import SkillGapAnalyzer
from backend.services.taxonomy_service import TaxonomyService
from backend.models.dossier import GapStatus, GapSeverity

def test_gap_analyzer_detects_matched_partial_and_missing():
    benchmark = ROLE_BENCHMARKS["junior machine learning engineer"]
    
    # Student has Python (Advanced -> Matched), PyTorch (Beginner -> Partial because Intermediate needed), and missing Docker
    profile = StudentProfile(
        name="Candidate A",
        email="a@test.com",
        education=Education(
            institution="MIT",
            degree="B.S.",
            major="CS",
            graduation_year=2026
        ),
        skills=[
            SkillItem(name="Python", proficiency=SkillProficiency.ADVANCED, category=SkillCategory.PROGRAMMING),
            SkillItem(name="PyTorch", proficiency=SkillProficiency.BEGINNER, category=SkillCategory.DATA_ML),
            SkillItem(name="Rust", proficiency=SkillProficiency.ADVANCED, category=SkillCategory.PROGRAMMING), # Differentiator
        ],
        career_goal=CareerGoal(target_role="Junior Machine Learning Engineer"),
        hours_per_week_available=10
    )

    report = SkillGapAnalyzer.analyze_profile(profile, benchmark)

    # Validate stats
    assert report.matched_skills_count >= 1 # Python
    assert report.partial_skills_count >= 1 # PyTorch
    assert report.missing_skills_count >= 1 # Docker, MLOps, SQL, etc.
    assert report.differentiator_skills_count >= 1 # Rust
    assert 0.0 <= report.overall_readiness_score <= 100.0

    # Check status of Python
    py_item = next(g for g in report.gaps if g.skill_name.lower() == "python")
    assert py_item.status == GapStatus.MATCHED
    assert py_item.severity == GapSeverity.NONE

    # Check status of PyTorch
    pt_item = next(g for g in report.gaps if g.skill_name.lower() == "pytorch")
    assert pt_item.status == GapStatus.PARTIAL

def test_taxonomy_normalization():
    assert TaxonomyService.normalize_skill_name("k8s") == "Kubernetes"
    assert TaxonomyService.normalize_skill_name("postgres") == "PostgreSQL"
    assert TaxonomyService.normalize_skill_name("docker") == "Docker Containers"
    assert TaxonomyService.normalize_skill_name("reactjs") == "React.js"
