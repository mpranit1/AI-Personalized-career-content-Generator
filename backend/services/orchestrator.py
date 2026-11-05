import uuid
from datetime import datetime, timezone

from backend.models.student import StudentProfile
from backend.models.dossier import UnifiedCareerDossier
from backend.services.taxonomy_service import TaxonomyService
from backend.services.gap_analyzer import SkillGapAnalyzer
from backend.services.generator import ProfileContentGenerator
from backend.services.formatters import FormattersService
from backend.services.consistency import ConsistencyAuditor
from backend.services.llm_provider import LLMProvider

class CareerDossierOrchestrator:
    def __init__(self):
        self.llm_provider = LLMProvider()

    def generate_dossier(self, profile: StudentProfile) -> UnifiedCareerDossier:
        dossier_id = str(uuid.uuid4())
        timestamp = datetime.now(timezone.utc).isoformat()

        # 1. Benchmark role resolution
        benchmark = TaxonomyService.get_or_synthesize_benchmark(
            target_role=profile.career_goal.target_role,
            academic_interests=profile.academic_interests,
        )

        # 2. Skill Gap Analysis
        gap_report = SkillGapAnalyzer.analyze_profile(profile, benchmark)

        # 3. Professional Summary Generation
        base_summary = ProfileContentGenerator.generate_professional_summary(
            profile=profile,
            benchmark=benchmark,
            gap_report=gap_report,
        )
        
        # Optional LLM polish if key is provided
        if self.llm_provider.is_available():
            final_summary = self.llm_provider.polish_summary_with_llm(base_summary, profile, benchmark)
            model_used = f"Google Gemini ({self.llm_provider.model_name}) + Knowledge Graph"
        else:
            final_summary = base_summary
            model_used = "Semantic Knowledge Graph & Ontology Engine"

        # 4. Learning Recommendations & Roadmap
        roadmap = ProfileContentGenerator.generate_learning_roadmap(
            profile=profile,
            benchmark=benchmark,
            gap_report=gap_report,
        )

        # 5. Interview Prep Package
        interview_prep = ProfileContentGenerator.generate_interview_prep(
            profile=profile,
            benchmark=benchmark,
            gap_report=gap_report,
        )

        # 6. Formatted Artifacts (Resume, LinkedIn, Study Guide, HTML Dossier)
        formatted = FormattersService.generate_all_formats(
            profile=profile,
            summary=final_summary,
            gap_report=gap_report,
            roadmap=roadmap,
            interview_prep=interview_prep,
        )

        # 7. Cross-Format Consistency Audit
        audit = ConsistencyAuditor.audit_dossier(
            profile=profile,
            summary=final_summary,
            gap_report=gap_report,
            roadmap=roadmap,
            interview_prep=interview_prep,
            formatted_artifacts={
                "markdown_resume": formatted.markdown_resume,
                "linkedin_profile_text": formatted.linkedin_profile_text,
                "career_dossier_html": formatted.career_dossier_html,
            },
        )

        return UnifiedCareerDossier(
            id=dossier_id,
            generated_at=timestamp,
            student_profile=profile,
            professional_summary=final_summary,
            skill_gap_report=gap_report,
            learning_roadmap=roadmap,
            interview_prep=interview_prep,
            consistency_audit=audit,
            formatted_artifacts=formatted,
            model_used=model_used,
        )

