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
from backend.services.consistency import ConsistencyAuditor
from backend.models.dossier import AuditCheckStatus

def test_full_dossier_consistency_audit_passes():
    profile = StudentProfile(
        name="Elena Rostova",
        email="elena@university.edu",
        education=Education(
            institution="University of Washington",
            degree="B.S.",
            major="Computer Science",
            graduation_year=2026,
            coursework=["Algorithms", "Distributed Systems"]
        ),
        skills=[
            SkillItem(name="Python", proficiency=SkillProficiency.ADVANCED),
            SkillItem(name="PyTorch", proficiency=SkillProficiency.INTERMEDIATE),
            SkillItem(name="SQL", proficiency=SkillProficiency.INTERMEDIATE),
        ],
        career_goal=CareerGoal(target_role="Junior Machine Learning Engineer"),
        projects=[
            Project(
                title="Neural Style Transfer App",
                description="Built neural style transfer with PyTorch and FastAPI.",
                tech_stack=["Python", "PyTorch", "FastAPI"],
                highlights=["Fast real-time filtering"]
            )
        ],
        hours_per_week_available=12
    )

    orchestrator = CareerDossierOrchestrator()
    dossier = orchestrator.generate_dossier(profile)
    audit = dossier.consistency_audit

    assert audit.overall_consistency_score >= 88.0
    assert audit.is_consistent is True

    # Check dimension scores
    assert audit.dimension_scores["role_alignment"] == 100.0
    assert audit.dimension_scores["gap_remediation_coverage"] == 100.0
    assert audit.dimension_scores["workload_realism"] == 100.0

def test_consistency_auditor_flags_mismatched_roles():
    profile = StudentProfile(
        name="Test Student",
        education=Education(institution="College", degree="B.S.", major="CS", graduation_year=2026),
        skills=[SkillItem(name="Python", proficiency=SkillProficiency.INTERMEDIATE)],
        career_goal=CareerGoal(target_role="Junior Machine Learning Engineer")
    )
    orchestrator = CareerDossierOrchestrator()
    dossier = orchestrator.generate_dossier(profile)

    # Intentionally corrupt summary target role to test audit detection
    tampered_summary = dossier.professional_summary.model_copy(update={"target_role": "Cybersecurity Penetration Tester"})

    audit_tampered = ConsistencyAuditor.audit_dossier(
        profile=profile,
        summary=tampered_summary,
        gap_report=dossier.skill_gap_report,
        roadmap=dossier.learning_roadmap,
        interview_prep=dossier.interview_prep
    )

    # Role alignment check must FAIL
    role_check = next(c for c in audit_tampered.audit_checks if c.dimension == "role_alignment")
    assert role_check.status == AuditCheckStatus.FAIL
    assert "Role mismatch detected" in role_check.details

