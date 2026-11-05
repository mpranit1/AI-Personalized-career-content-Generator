from typing import List, Dict, Optional, Any
from enum import Enum
from pydantic import BaseModel, Field
from backend.models.student import StudentProfile

class GapStatus(str, Enum):
    MATCHED = "matched"
    PARTIAL = "partial"
    MISSING = "missing"
    DIFFERENTIATOR = "differentiator"

class GapSeverity(str, Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    NONE = "none"

class SkillGapItem(BaseModel):
    skill_name: str
    category: str
    status: GapStatus
    current_proficiency: Optional[str] = None
    required_proficiency: str
    severity: GapSeverity
    importance_weight: float = Field(default=1.0, description="1.0 to 3.0 scale for readiness weighting")
    impact_analysis: str
    remediation_priority: int = Field(default=1, description="1 is highest priority")

class SkillGapReport(BaseModel):
    target_role: str
    seniority: str
    overall_readiness_score: float = Field(..., ge=0.0, le=100.0, description="Readiness percentage 0-100")
    category_scores: Dict[str, float] = Field(default_factory=dict, description="Category percentage scores")
    total_required_skills: int
    matched_skills_count: int
    partial_skills_count: int
    missing_skills_count: int
    differentiator_skills_count: int = 0
    readiness_tier: str = Field(..., description="e.g. 'Interview Ready', 'Accelerated Growth Needed', 'Foundation Building'")
    gaps: List[SkillGapItem]
    top_priority_gaps: List[str]
    readiness_assessment: str

class ProfessionalSummary(BaseModel):
    target_role: str
    headline: str
    alternative_headlines: List[str] = Field(default_factory=list)
    executive_summary: str = Field(..., description="Concise 3-4 sentence resume summary")
    linkedin_about: str = Field(..., description="Narrative first-person summary with competencies and achievements")
    elevator_pitch_30s: str = Field(..., description="Spoken verbal intro for career fairs & networking")
    key_value_propositions: List[str] = Field(default_factory=list, description="3-4 bulleted competitive advantages")
    core_competencies: List[str] = Field(default_factory=list, description="Top skills highlighted across the summary")

class CuratedResource(BaseModel):
    title: str
    resource_type: str = Field(..., description="Course, Documentation, Book, Project, or Certification")
    url_or_platform: str
    estimated_hours: int
    difficulty: str = Field(default="Intermediate")

class LearningRecommendationItem(BaseModel):
    gap_skill: str
    category: str
    severity: GapSeverity
    priority_order: int
    target_proficiency: str
    recommended_action: str
    curated_resources: List[CuratedResource] = Field(default_factory=list)
    capstone_mini_project: str = Field(..., description="Concrete project idea to demonstrate mastery")
    verification_deliverable: str = Field(..., description="Specific artifact, e.g. GitHub repo with CI/CD, benchmark test suite")
    estimated_weeks: int

class RoadmapPhase(BaseModel):
    phase_number: int
    phase_name: str
    duration_weeks: int
    focus_summary: str
    recommendations: List[LearningRecommendationItem]

class LearningRoadmap(BaseModel):
    target_role: str
    total_weeks: int
    weekly_hours: int
    total_study_hours: int
    phases: List[RoadmapPhase]
    suggested_certifications: List[str] = Field(default_factory=list)
    milestone_deliverables: List[str] = Field(default_factory=list)

class QuestionCategory(str, Enum):
    TECHNICAL = "technical"
    BEHAVIORAL_STAR = "behavioral_star"
    PROJECT_DEFENSE = "project_defense"
    SYSTEM_DESIGN = "system_design"

class StarStoryBreakdown(BaseModel):
    situation: str
    task: str
    action: str
    result: str

class InterviewQuestion(BaseModel):
    id: str
    category: QuestionCategory
    topic: str
    question: str
    context_or_scenario: Optional[str] = None
    sample_ideal_answer: str
    key_concepts_to_demonstrate: List[str]
    pitfalls_to_avoid: List[str]
    star_breakdown: Optional[StarStoryBreakdown] = None
    referenced_student_project: Optional[str] = None

class InterviewPrepPackage(BaseModel):
    target_role: str
    technical_questions: List[InterviewQuestion]
    behavioral_questions: List[InterviewQuestion]
    project_defense_questions: List[InterviewQuestion]
    system_design_questions: List[InterviewQuestion] = Field(default_factory=list)
    day_before_cheat_sheet: List[str] = Field(default_factory=list)
    interviewer_red_flags: List[str] = Field(default_factory=list)

class AuditCheckStatus(str, Enum):
    PASS = "PASS"
    WARN = "WARN"
    FAIL = "FAIL"

class ConsistencyAuditCheck(BaseModel):
    check_name: str
    dimension: str
    status: AuditCheckStatus
    details: str
    evidence: Optional[Dict[str, Any]] = None

class ConsistencyAuditResult(BaseModel):
    overall_consistency_score: float = Field(..., ge=0.0, le=100.0)
    is_consistent: bool
    dimension_scores: Dict[str, float]
    audit_checks: List[ConsistencyAuditCheck]
    reconciliation_notes: List[str] = Field(default_factory=list)

class FormattedArtifacts(BaseModel):
    markdown_resume: str
    linkedin_profile_text: str
    career_dossier_html: str
    interview_study_sheet_markdown: str

class UnifiedCareerDossier(BaseModel):
    id: str
    generated_at: str
    student_profile: StudentProfile
    professional_summary: ProfessionalSummary
    skill_gap_report: SkillGapReport
    learning_roadmap: LearningRoadmap
    interview_prep: InterviewPrepPackage
    consistency_audit: ConsistencyAuditResult
    formatted_artifacts: FormattedArtifacts
    model_used: str = "Hybrid Knowledge Graph Engine + LLM"
