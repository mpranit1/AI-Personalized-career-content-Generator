import pytest
from backend.models.student import (
    StudentProfile,
    Education,
    SkillItem,
    SkillProficiency,
    CareerGoal,
    Project,
)
from backend.services.orchestrator import CareerDossierOrchestrator
from backend.services.taxonomy_service import TaxonomyService
from backend.models.dossier import QuestionCategory

def test_generator_synthesizes_custom_niche_roles():
    # Test arbitrary non-catalog role
    profile = StudentProfile(
        name="Sam Bio",
        education=Education(institution="Johns Hopkins", degree="M.S.", major="Bioinformatics", graduation_year=2026),
        skills=[
            SkillItem(name="Python", proficiency=SkillProficiency.ADVANCED),
            SkillItem(name="R", proficiency=SkillProficiency.INTERMEDIATE),
        ],
        career_goal=CareerGoal(target_role="Genomic Data Pipeline Specialist"),
        academic_interests=["Next-Gen Sequencing", "Variant Calling Algorithms"],
        hours_per_week_available=15
    )

    orchestrator = CareerDossierOrchestrator()
    dossier = orchestrator.generate_dossier(profile)

    assert dossier.professional_summary.target_role == "Genomic Data Pipeline Specialist"
    assert "Sam Bio" in dossier.professional_summary.elevator_pitch_30s
    assert "Genomic Data Pipeline Specialist" in dossier.professional_summary.executive_summary
    assert len(dossier.learning_roadmap.phases) >= 2
    assert len(dossier.interview_prep.technical_questions) >= 2
    assert len(dossier.interview_prep.behavioral_questions) >= 1

def test_interview_prep_structure():
    profile = StudentProfile(
        name="Developer One",
        education=Education(institution="Georgia Tech", degree="B.S.", major="CS", graduation_year=2025),
        skills=[SkillItem(name="Python", proficiency=SkillProficiency.INTERMEDIATE)],
        career_goal=CareerGoal(target_role="Backend Software Engineer"),
        projects=[
            Project(
                title="Distributed Cache Layer",
                description="Built an LRU cache with Redis backend.",
                tech_stack=["Python", "Redis"]
            )
        ]
    )

    orchestrator = CareerDossierOrchestrator()
    dossier = orchestrator.generate_dossier(profile)
    prep = dossier.interview_prep

    assert len(prep.technical_questions) > 0
    assert len(prep.behavioral_questions) > 0
    assert len(prep.project_defense_questions) > 0

    # Ensure project defense refers to the project
    proj_defense = prep.project_defense_questions[0]
    assert "Distributed Cache Layer" in proj_defense.question or proj_defense.referenced_student_project == "Distributed Cache Layer"
