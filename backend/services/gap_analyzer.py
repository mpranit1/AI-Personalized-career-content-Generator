from typing import List, Dict, Tuple
from collections import defaultdict

from backend.models.student import StudentProfile, SkillItem
from backend.models.dossier import (
    SkillGapReport,
    SkillGapItem,
    GapStatus,
    GapSeverity,
)
from backend.models.career_data import RoleBenchmark, RoleSkillRequirement
from backend.services.taxonomy_service import TaxonomyService

class SkillGapAnalyzer:
    @classmethod
    def analyze_profile(cls, profile: StudentProfile, benchmark: RoleBenchmark) -> SkillGapReport:
        student_skill_map: Dict[str, SkillItem] = {}
        for s in profile.skills:
            norm_name = TaxonomyService.normalize_skill_name(s.name)
            student_skill_map[norm_name.lower()] = s

        gap_items: List[SkillGapItem] = []
        matched_count = 0
        partial_count = 0
        missing_count = 0

        total_weight = 0.0
        earned_weight = 0.0

        category_total_weights = defaultdict(float)
        category_earned_weights = defaultdict(float)

        # 1. Compare against role benchmark requirements
        for req in benchmark.skills:
            req_norm = TaxonomyService.normalize_skill_name(req.name).lower()
            req_rank = TaxonomyService.get_proficiency_rank(req.required_proficiency)
            weight = req.weight
            total_weight += weight
            category_total_weights[req.category] += weight

            student_skill = student_skill_map.get(req_norm)

            if student_skill:
                curr_rank = TaxonomyService.get_proficiency_rank(student_skill.proficiency.value)
                if curr_rank >= req_rank:
                    status = GapStatus.MATCHED
                    severity = GapSeverity.NONE
                    matched_count += 1
                    earned_weight += weight
                    category_earned_weights[req.category] += weight
                    impact = f"Strong match: Currently at '{student_skill.proficiency.value}' level, fulfilling the benchmark requirement."
                else:
                    status = GapStatus.PARTIAL
                    severity = GapSeverity.HIGH if req.importance == "critical" else GapSeverity.MEDIUM
                    partial_count += 1
                    # Partial credit (e.g. 50% credit for having beginner when intermediate needed)
                    partial_ratio = max(0.3, curr_rank / req_rank)
                    earned_weight += weight * partial_ratio
                    category_earned_weights[req.category] += weight * partial_ratio
                    impact = f"Developing capability: Has '{student_skill.proficiency.value}', but {benchmark.canonical_title} demands '{req.required_proficiency}' level. {req.impact_rationale}"
            else:
                status = GapStatus.MISSING
                if req.importance == "critical":
                    severity = GapSeverity.CRITICAL
                elif req.importance == "high":
                    severity = GapSeverity.HIGH
                else:
                    severity = GapSeverity.MEDIUM
                missing_count += 1
                impact = f"Key gap identified: Missing from profile. {req.impact_rationale}"

            gap_items.append(
                SkillGapItem(
                    skill_name=req.name,
                    category=req.category,
                    status=status,
                    current_proficiency=student_skill.proficiency.value if student_skill else None,
                    required_proficiency=req.required_proficiency,
                    severity=severity,
                    importance_weight=weight,
                    impact_analysis=impact,
                    remediation_priority=1 if severity == GapSeverity.CRITICAL else (2 if severity == GapSeverity.HIGH else 3),
                )
            )

        # 2. Identify differentiator skills
        req_names_set = {TaxonomyService.normalize_skill_name(req.name).lower() for req in benchmark.skills}
        differentiator_count = 0
        for s in profile.skills:
            norm_name = TaxonomyService.normalize_skill_name(s.name).lower()
            if norm_name not in req_names_set:
                differentiator_count += 1
                gap_items.append(
                    SkillGapItem(
                        skill_name=s.name,
                        category=s.category.value if s.category else "Bonus & Complementary",
                        status=GapStatus.DIFFERENTIATOR,
                        current_proficiency=s.proficiency.value,
                        required_proficiency="Bonus / Value-Add",
                        severity=GapSeverity.NONE,
                        importance_weight=1.0,
                        impact_analysis=f"Competitive differentiator: Gives an edge over other applicants for {benchmark.canonical_title}.",
                        remediation_priority=99,
                    )
                )

        # 3. Calculate scores
        raw_score = (earned_weight / total_weight * 100.0) if total_weight > 0 else 50.0
        # Boost slightly for differentiators (up to 5% bonus capped at 100)
        final_score = min(100.0, round(raw_score + min(5.0, differentiator_count * 1.5), 1))

        category_scores: Dict[str, float] = {}
        for cat, t_w in category_total_weights.items():
            e_w = category_earned_weights[cat]
            category_scores[cat] = round((e_w / t_w * 100.0), 1) if t_w > 0 else 100.0

        # Sort gaps: Critical first, then High, then Medium, then Matched, then Differentiator
        severity_order = {
            GapSeverity.CRITICAL: 0,
            GapSeverity.HIGH: 1,
            GapSeverity.MEDIUM: 2,
            GapSeverity.LOW: 3,
            GapSeverity.NONE: 4,
        }
        gap_items.sort(key=lambda item: (severity_order.get(item.severity, 5), -item.importance_weight))

        top_priority_gaps = [
            item.skill_name for item in gap_items if item.severity in (GapSeverity.CRITICAL, GapSeverity.HIGH)
        ]

        # Tier calculation
        if final_score >= 85:
            tier = "Interview Ready (Top Quartile Candidate)"
            assessment = f"Excellent alignment with {benchmark.canonical_title}. Your foundation covers core competencies; focus on polishing edge cases, system design tradeoffs, and mock interviews."
        elif final_score >= 70:
            tier = "Fast-Track Candidate (4-6 Weeks to Prime Readiness)"
            assessment = f"Strong baseline skills present for {benchmark.canonical_title}. Bridging {len(top_priority_gaps)} key skill gap(s) will position you strongly for competitive hiring rounds."
        elif final_score >= 50:
            tier = "Accelerated Upskilling (8-12 Weeks Structured Roadmap)"
            assessment = f"Solid academic foundation with clear practical growth opportunities. Following the prioritized learning roadmap will systematically eliminate bottlenecks in your technical profile."
        else:
            tier = "Foundational Growth (Core Competency Building)"
            assessment = f"Initial phase of transition into {benchmark.canonical_title}. Focus first on core languages, foundational projects, and hands-on laboratory exercises."

        return SkillGapReport(
            target_role=benchmark.canonical_title,
            seniority=benchmark.standard_seniority,
            overall_readiness_score=final_score,
            category_scores=category_scores,
            total_required_skills=len(benchmark.skills),
            matched_skills_count=matched_count,
            partial_skills_count=partial_count,
            missing_skills_count=missing_count,
            differentiator_skills_count=differentiator_count,
            readiness_tier=tier,
            gaps=gap_items,
            top_priority_gaps=top_priority_gaps,
            readiness_assessment=assessment,
        )
