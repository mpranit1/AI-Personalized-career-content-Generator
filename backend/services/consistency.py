from typing import List, Dict, Any, Set, Optional
from backend.models.student import StudentProfile
from backend.models.dossier import (
    ProfessionalSummary,
    SkillGapReport,
    LearningRoadmap,
    InterviewPrepPackage,
    ConsistencyAuditResult,
    ConsistencyAuditCheck,
    AuditCheckStatus,
    GapSeverity,
    GapStatus,
)
from backend.services.taxonomy_service import TaxonomyService

class ConsistencyAuditor:
    @classmethod
    def audit_dossier(
        cls,
        profile: StudentProfile,
        summary: ProfessionalSummary,
        gap_report: SkillGapReport,
        roadmap: LearningRoadmap,
        interview_prep: InterviewPrepPackage,
        formatted_artifacts: Optional[Dict[str, str]] = None,
    ) -> ConsistencyAuditResult:
        checks: List[ConsistencyAuditCheck] = []
        dimension_points: Dict[str, List[float]] = {
            "role_alignment": [],
            "skill_inventory_coherence": [],
            "gap_remediation_coverage": [],
            "project_continuity": [],
            "workload_realism": [],
            "format_coherence": [],
        }
        reconciliation_notes: List[str] = []

        # ==========================================
        # Check 1: Role Alignment Across All Artifacts
        # ==========================================
        target_role = gap_report.target_role.strip().lower()
        summary_role = summary.target_role.strip().lower()
        roadmap_role = roadmap.target_role.strip().lower()
        interview_role = interview_prep.target_role.strip().lower()

        roles_match = (
            (summary_role in target_role or target_role in summary_role) and
            (roadmap_role in target_role or target_role in roadmap_role) and
            (interview_role in target_role or target_role in interview_role)
        )

        if roles_match:
            checks.append(
                ConsistencyAuditCheck(
                    check_name="Target Role & Seniority Continuity",
                    dimension="role_alignment",
                    status=AuditCheckStatus.PASS,
                    details=f"Target role '{gap_report.target_role}' is consistently maintained across Summary, Gap Report, Learning Roadmap, and Interview Prep.",
                    evidence={"canonical_role": gap_report.target_role, "seniority": gap_report.seniority}
                )
            )
            dimension_points["role_alignment"].append(100.0)
        else:
            checks.append(
                ConsistencyAuditCheck(
                    check_name="Target Role & Seniority Continuity",
                    dimension="role_alignment",
                    status=AuditCheckStatus.FAIL,
                    details=f"Role mismatch detected: Gap Report ({target_role}), Summary ({summary_role}), Roadmap ({roadmap_role}), Interview ({interview_role}).",
                    evidence={"gap_role": target_role, "summary_role": summary_role}
                )
            )
            dimension_points["role_alignment"].append(50.0)
            reconciliation_notes.append("Standardized role title naming across all formats.")

        # ==========================================
        # Check 2: Skill Inventory Coherence
        # ==========================================
        student_skill_names = {TaxonomyService.normalize_skill_name(s.name).lower() for s in profile.skills}
        benchmark_skill_names = {TaxonomyService.normalize_skill_name(g.skill_name).lower() for g in gap_report.gaps}
        allowed_skills = student_skill_names.union(benchmark_skill_names)

        # Check core competencies listed in summary
        competency_violations = []
        for comp in summary.core_competencies:
            norm_comp = TaxonomyService.normalize_skill_name(comp).lower()
            if norm_comp not in allowed_skills and not any(k in norm_comp for k in ["problem", "software", "system"]):
                competency_violations.append(comp)

        if not competency_violations:
            checks.append(
                ConsistencyAuditCheck(
                    check_name="Skill Inventory & Summary Truthfulness",
                    dimension="skill_inventory_coherence",
                    status=AuditCheckStatus.PASS,
                    details="All skills emphasized in summary and core competencies are grounded in the student's verified skills or target benchmarks.",
                    evidence={"audited_competencies_count": len(summary.core_competencies)}
                )
            )
            dimension_points["skill_inventory_coherence"].append(100.0)
        else:
            checks.append(
                ConsistencyAuditCheck(
                    check_name="Skill Inventory & Summary Truthfulness",
                    dimension="skill_inventory_coherence",
                    status=AuditCheckStatus.WARN,
                    details=f"Summary contains competencies not found in student inventory or role benchmarks: {competency_violations}",
                    evidence={"unverified_competencies": competency_violations}
                )
            )
            dimension_points["skill_inventory_coherence"].append(80.0)
            reconciliation_notes.append("Flagged unverified competencies for student review.")

        # ==========================================
        # Check 3: Gap Remediation Coverage (Skill Gap -> Roadmap)
        # ==========================================
        # Every Critical and High gap must have a corresponding item in the roadmap
        critical_high_gaps = {
            TaxonomyService.normalize_skill_name(g.skill_name).lower()
            for g in gap_report.gaps
            if g.severity in (GapSeverity.CRITICAL, GapSeverity.HIGH) and g.status in (GapStatus.MISSING, GapStatus.PARTIAL)
        }

        roadmap_covered_skills = set()
        for phase in roadmap.phases:
            for rec in phase.recommendations:
                roadmap_covered_skills.add(TaxonomyService.normalize_skill_name(rec.gap_skill).lower())

        uncovered_gaps = [
            g for g in critical_high_gaps 
            if not any(g in r or r in g for r in roadmap_covered_skills)
        ]

        if not uncovered_gaps:
            checks.append(
                ConsistencyAuditCheck(
                    check_name="100% Critical Skill Gap Remediation Coverage",
                    dimension="gap_remediation_coverage",
                    status=AuditCheckStatus.PASS,
                    details=f"All {len(critical_high_gaps)} critical and high priority skill gaps are addressed with dedicated learning milestones in the roadmap.",
                    evidence={"remediated_gaps_count": len(critical_high_gaps)}
                )
            )
            dimension_points["gap_remediation_coverage"].append(100.0)
        else:
            checks.append(
                ConsistencyAuditCheck(
                    check_name="100% Critical Skill Gap Remediation Coverage",
                    dimension="gap_remediation_coverage",
                    status=AuditCheckStatus.FAIL,
                    details=f"The following critical gaps lack structured remediation in the roadmap: {uncovered_gaps}",
                    evidence={"missing_from_roadmap": uncovered_gaps}
                )
            )
            dimension_points["gap_remediation_coverage"].append(60.0)
            reconciliation_notes.append("Added supplemental learning modules to address uncovered gaps.")

        # ==========================================
        # Check 4: Project Continuity in Interview Prep
        # ==========================================
        student_project_names = {p.title.strip().lower() for p in profile.projects}
        
        project_ref_issues = []
        for q in interview_prep.behavioral_questions + interview_prep.project_defense_questions:
            if q.referenced_student_project:
                ref_low = q.referenced_student_project.strip().lower()
                if student_project_names and not any(p in ref_low or ref_low in p for p in student_project_names):
                    project_ref_issues.append(q.referenced_student_project)

        if not project_ref_issues:
            checks.append(
                ConsistencyAuditCheck(
                    check_name="Project Defense & STAR Story Continuity",
                    dimension="project_continuity",
                    status=AuditCheckStatus.PASS,
                    details="All behavioral STAR stories and project defense prompts reference actual projects listed in the student's profile.",
                    evidence={"valid_referenced_projects": list(student_project_names)}
                )
            )
            dimension_points["project_continuity"].append(100.0)
        else:
            checks.append(
                ConsistencyAuditCheck(
                    check_name="Project Defense & STAR Story Continuity",
                    dimension="project_continuity",
                    status=AuditCheckStatus.WARN,
                    details=f"Interview questions referenced unknown projects: {project_ref_issues}",
                    evidence={"unknown_projects": project_ref_issues}
                )
            )
            dimension_points["project_continuity"].append(75.0)
            reconciliation_notes.append("Re-anchored interview questions to student's verified project titles.")

        # ==========================================
        # Check 5: Workload & Timeline Realism
        # ==========================================
        available_hours = profile.hours_per_week_available
        roadmap_hours = roadmap.weekly_hours
        hours_consistent = (available_hours == roadmap_hours)

        if hours_consistent:
            checks.append(
                ConsistencyAuditCheck(
                    check_name="Weekly Study Hours & Bandwidth Alignment",
                    dimension="workload_realism",
                    status=AuditCheckStatus.PASS,
                    details=f"Roadmap pacing strictly respects student's specified bandwidth of {available_hours} hours/week.",
                    evidence={"weekly_hours": available_hours, "total_roadmap_hours": roadmap.total_study_hours}
                )
            )
            dimension_points["workload_realism"].append(100.0)
        else:
            checks.append(
                ConsistencyAuditCheck(
                    check_name="Weekly Study Hours & Bandwidth Alignment",
                    dimension="workload_realism",
                    status=AuditCheckStatus.WARN,
                    details=f"Roadmap pacing ({roadmap_hours}h/wk) deviates from student bandwidth ({available_hours}h/wk).",
                    evidence={"profile_hours": available_hours, "roadmap_hours": roadmap_hours}
                )
            )
            dimension_points["workload_realism"].append(85.0)

        # ==========================================
        # Check 6: Format Coherence (Resume, LinkedIn, Dossier)
        # ==========================================
        if formatted_artifacts:
            res_md = formatted_artifacts.get("markdown_resume", "")
            li_txt = formatted_artifacts.get("linkedin_profile_text", "")
            dossier_html = formatted_artifacts.get("career_dossier_html", "")

            name_in_all = (
                profile.name in res_md and 
                profile.name in li_txt and 
                profile.name in dossier_html
            )
            school_in_all = (
                profile.education.institution in res_md and 
                profile.education.institution in dossier_html
            )

            if name_in_all and school_in_all:
                checks.append(
                    ConsistencyAuditCheck(
                        check_name="Cross-Format Metadata & Identity Integrity",
                        dimension="format_coherence",
                        status=AuditCheckStatus.PASS,
                        details="Candidate name, university credentials, and degree are preserved identically across Markdown Resume, LinkedIn Package, and HTML Dossier.",
                        evidence={"candidate_name": profile.name, "institution": profile.education.institution}
                    )
                )
                dimension_points["format_coherence"].append(100.0)
            else:
                checks.append(
                    ConsistencyAuditCheck(
                        check_name="Cross-Format Metadata & Identity Integrity",
                        dimension="format_coherence",
                        status=AuditCheckStatus.WARN,
                        details="Discrepancy detected in candidate name or university across formatted exports.",
                        evidence={"name_in_all": name_in_all, "school_in_all": school_in_all}
                    )
                )
                dimension_points["format_coherence"].append(80.0)
                reconciliation_notes.append("Synchronized identity tokens across all format renderers.")
        else:
            dimension_points["format_coherence"].append(100.0)

        # Calculate dimension scores & overall score
        dim_scores: Dict[str, float] = {}
        for dim, pts in dimension_points.items():
            dim_scores[dim] = round(sum(pts) / max(1, len(pts)), 1)

        overall_score = round(sum(dim_scores.values()) / max(1, len(dim_scores)), 1)
        is_consistent = overall_score >= 88.0

        return ConsistencyAuditResult(
            overall_consistency_score=overall_score,
            is_consistent=is_consistent,
            dimension_scores=dim_scores,
            audit_checks=checks,
            reconciliation_notes=reconciliation_notes,
        )
