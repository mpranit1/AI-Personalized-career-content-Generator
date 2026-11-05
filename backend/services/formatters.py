import json
from typing import Dict, Any
from backend.models.student import StudentProfile
from backend.models.dossier import (
    ProfessionalSummary,
    SkillGapReport,
    LearningRoadmap,
    InterviewPrepPackage,
    ConsistencyAuditResult,
    FormattedArtifacts,
)

class FormattersService:
    @classmethod
    def generate_all_formats(
        cls,
        profile: StudentProfile,
        summary: ProfessionalSummary,
        gap_report: SkillGapReport,
        roadmap: LearningRoadmap,
        interview_prep: InterviewPrepPackage,
    ) -> FormattedArtifacts:
        md_resume = cls.render_markdown_resume(profile, summary)
        linkedin_pack = cls.render_linkedin_package(profile, summary)
        interview_guide = cls.render_interview_study_sheet(profile, interview_prep)
        dossier_html = cls.render_career_dossier_html(profile, summary, gap_report, roadmap, interview_prep)

        return FormattedArtifacts(
            markdown_resume=md_resume,
            linkedin_profile_text=linkedin_pack,
            career_dossier_html=dossier_html,
            interview_study_sheet_markdown=interview_guide,
        )

    @classmethod
    def render_markdown_resume(cls, profile: StudentProfile, summary: ProfessionalSummary) -> str:
        edu = profile.education
        tech_skills = [f"{s.name} ({s.proficiency.value.title()})" for s in profile.skills]
        
        projects_md = ""
        for p in profile.projects:
            stack_str = f" | *{', '.join(p.tech_stack)}*" if p.tech_stack else ""
            link_str = f" | [Demo/Repo]({p.link})" if p.link else ""
            hl_str = ""
            for h in p.highlights:
                hl_str += f"\n- {h}"
            if not hl_str:
                hl_str = f"\n- {p.description}"
            projects_md += f"""
### {p.title}{stack_str}{link_str}
*{p.role or 'Developer'}*{hl_str}
"""

        coursework_str = f"\n**Relevant Coursework:** {', '.join(edu.coursework)}" if edu.coursework else ""
        gpa_str = f" | GPA: {edu.gpa}" if edu.gpa else ""
        honors_str = f"\n**Honors:** {', '.join(edu.honors)}" if edu.honors else ""

        return f"""# {profile.name}
**{summary.headline}**  
Email: {profile.email} | Location: {profile.location} | Target: {summary.target_role}

---

## PROFESSIONAL SUMMARY
{summary.executive_summary}

---

## TECHNICAL SKILLS & CORE COMPETENCIES
- **Core Skills:** {', '.join(tech_skills)}
- **Key Competencies:** {', '.join(summary.core_competencies)}
- **Areas of Interest:** {', '.join(profile.academic_interests) if profile.academic_interests else summary.target_role}

---

## EDUCATION
### {edu.institution}
**{edu.degree} in {edu.major}** | Class of {edu.graduation_year}{gpa_str}{coursework_str}{honors_str}

---

## TECHNICAL PROJECTS
{projects_md.strip()}
"""

    @classmethod
    def render_linkedin_package(cls, profile: StudentProfile, summary: ProfessionalSummary) -> str:
        top_skills = [s.name for s in profile.skills[:5]]
        
        alt_headlines_md = "\n".join([f"- Option {i+1}: {h}" for i, h in enumerate(summary.alternative_headlines)])

        featured_projects_md = ""
        for p in profile.projects[:3]:
            featured_projects_md += f"""
• {p.title}
  Tagline: Built using {', '.join(p.tech_stack)}
  Description: {p.description}
"""

        return f"""================================================================================
LINKEDIN OPTIMIZATION PACKAGE FOR {profile.name.upper()}
Target Role: {summary.target_role}
================================================================================

1. PRIMARY HEADLINE (Recommended):
{summary.headline}

ALTERNATIVE HEADLINES:
{alt_headlines_md}

--------------------------------------------------------------------------------
2. ABOUT SECTION:
{summary.linkedin_about}

--------------------------------------------------------------------------------
3. TOP 5 SKILLS TO PIN FOR ENDORSEMENTS:
{', '.join(top_skills)}

--------------------------------------------------------------------------------
4. FEATURED SECTION SPOTLIGHT:
{featured_projects_md.strip()}

--------------------------------------------------------------------------------
5. 30-SECOND VERBAL ELEVATOR PITCH (For Networking & InMails):
"{summary.elevator_pitch_30s}"
================================================================================
"""

    @classmethod
    def render_interview_study_sheet(cls, profile: StudentProfile, interview_prep: InterviewPrepPackage) -> str:
        tech_q_md = ""
        for i, q in enumerate(interview_prep.technical_questions, 1):
            tech_q_md += f"""
### Question {i}: {q.question}
- **Topic / Domain:** {q.topic}
- **Key Concepts to Demonstrate:** {', '.join(q.key_concepts_to_demonstrate)}
- **Model Answer:**
> {q.sample_ideal_answer}
- **Pitfalls to Avoid:** {', '.join(q.pitfalls_to_avoid)}
"""

        beh_q_md = ""
        for i, q in enumerate(interview_prep.behavioral_questions, 1):
            star_txt = ""
            if q.star_breakdown:
                star_txt = f"""
  - **Situation:** {q.star_breakdown.situation}
  - **Task:** {q.star_breakdown.task}
  - **Action:** {q.star_breakdown.action}
  - **Result:** {q.star_breakdown.result}"""
            beh_q_md += f"""
### Behavioral Question {i}: {q.question}
- **Theme:** {q.topic}
- **STAR Response Framework:**{star_txt}
- **Sample Articulation:** {q.sample_ideal_answer}
"""

        proj_q_md = ""
        for i, q in enumerate(interview_prep.project_defense_questions, 1):
            proj_q_md += f"""
### Project Defense {i}: {q.question}
- **Project Focus:** {q.referenced_student_project or 'Architecture'}
- **Expected Rationale:** {q.sample_ideal_answer}
- **Trap / Pitfall to Avoid:** {', '.join(q.pitfalls_to_avoid)}
"""

        cheat_sheet_md = "\n".join([f"- {tip}" for tip in interview_prep.day_before_cheat_sheet])
        red_flags_md = "\n".join([f"- ⚠️ {rf}" for rf in interview_prep.interviewer_red_flags])

        return f"""# {interview_prep.target_role} Technical & Behavioral Interview Prep Sheet
**Candidate:** {profile.name} | **Target Role:** {interview_prep.target_role}

---

## 1. 24-HOUR EMERGENCY CHEAT SHEET
{cheat_sheet_md}

## RED FLAGS TO AVOID IN CONVERSATION
{red_flags_md}

---

## 2. TECHNICAL QUESTIONS & MODEL SOLUTIONS
{tech_q_md.strip()}

---

## 3. BEHAVIORAL QUESTIONS (STAR METHOD)
{beh_q_md.strip()}

---

## 4. PROJECT ARCHITECTURE DEFENSE
{proj_q_md.strip()}
"""

    @classmethod
    def render_career_dossier_html(
        cls,
        profile: StudentProfile,
        summary: ProfessionalSummary,
        gap_report: SkillGapReport,
        roadmap: LearningRoadmap,
        interview_prep: InterviewPrepPackage,
    ) -> str:
        # Generate an elegant, clean HTML report styled for screen and high-resolution print/PDF
        gaps_rows = ""
        for g in gap_report.gaps:
            status_color = "#10b981" if g.status.value == "matched" else ("#f59e0b" if g.status.value == "partial" else ("#3b82f6" if g.status.value == "differentiator" else "#ef4444"))
            status_badge = f'<span style="background:{status_color}20; color:{status_color}; font-weight:600; padding:3px 8px; border-radius:12px; font-size:12px;">{g.status.value.upper()}</span>'
            gaps_rows += f"""
            <tr>
                <td style="padding:10px; border-bottom:1px solid #e2e8f0; font-weight:600;">{g.skill_name}</td>
                <td style="padding:10px; border-bottom:1px solid #e2e8f0;">{g.category}</td>
                <td style="padding:10px; border-bottom:1px solid #e2e8f0;">{status_badge}</td>
                <td style="padding:10px; border-bottom:1px solid #e2e8f0;">{g.current_proficiency or '—'}</td>
                <td style="padding:10px; border-bottom:1px solid #e2e8f0; font-weight:500;">{g.required_proficiency}</td>
                <td style="padding:10px; border-bottom:1px solid #e2e8f0; font-size:13px; color:#475569;">{g.impact_analysis}</td>
            </tr>
            """

        roadmap_phases_html = ""
        for p in roadmap.phases:
            recs_html = ""
            for r in p.recommendations:
                recs_html += f"""
                <div style="background:#f8fafc; border-left:4px solid #3b82f6; padding:12px; margin-bottom:10px; border-radius:4px;">
                    <div style="font-weight:600; color:#1e293b;">{r.gap_skill} <span style="font-size:12px; color:#64748b; font-weight:normal;">({r.target_proficiency} target)</span></div>
                    <div style="font-size:13px; color:#334155; margin-top:4px;"><strong>Action:</strong> {r.recommended_action}</div>
                    <div style="font-size:13px; color:#0284c7; margin-top:4px;"><strong>Deliverable:</strong> {r.verification_deliverable}</div>
                </div>
                """
            roadmap_phases_html += f"""
            <div style="margin-bottom:20px; border:1px solid #e2e8f0; border-radius:8px; padding:16px;">
                <div style="font-size:16px; font-weight:700; color:#0f172a; margin-bottom:6px;">Phase {p.phase_number}: {p.phase_name} ({p.duration_weeks} Weeks)</div>
                <div style="font-size:13px; color:#64748b; margin-bottom:12px;">{p.focus_summary}</div>
                {recs_html}
            </div>
            """

        return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Career Readiness Dossier - {profile.name}</title>
<style>
    body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; color: #1e293b; line-height: 1.5; margin: 0; padding: 24px; background: #fff; }}
    .header {{ border-bottom: 2px solid #0f172a; padding-bottom: 16px; margin-bottom: 24px; display: flex; justify-content: space-between; align-items: flex-start; }}
    .badge {{ background: #e0f2fe; color: #0369a1; padding: 4px 10px; border-radius: 6px; font-size: 13px; font-weight: 600; display: inline-block; }}
    .score-box {{ background: #f0fdf4; border: 1px solid #bbf7d0; color: #166534; padding: 12px 20px; border-radius: 8px; text-align: center; }}
    .score-number {{ font-size: 32px; font-weight: 800; }}
    .section-title {{ font-size: 18px; font-weight: 700; color: #0f172a; margin-top: 32px; margin-bottom: 12px; border-bottom: 1px solid #e2e8f0; padding-bottom: 6px; }}
    table {{ width: 100%; border-collapse: collapse; font-size: 14px; text-align: left; }}
    th {{ background: #f1f5f9; padding: 10px; font-weight: 600; border-bottom: 2px solid #cbd5e1; }}
    @media print {{ body {{ padding: 0; font-size: 12px; }} .no-print {{ display: none; }} }}
</style>
</head>
<body>

<div class="header">
    <div>
        <h1 style="margin:0 0 6px 0; font-size:26px; color:#0f172a;">{profile.name}</h1>
        <div style="font-size:14px; color:#475569;">
            {profile.education.degree} in {profile.education.major} &bull; {profile.education.institution} &bull; Class of {profile.education.graduation_year}
        </div>
        <div style="margin-top:8px;">
            <span class="badge">Target Role: {summary.target_role}</span>
            <span class="badge" style="background:#fef3c7; color:#92400e; margin-left:8px;">{gap_report.readiness_tier}</span>
        </div>
    </div>
    <div class="score-box">
        <div class="score-number">{gap_report.overall_readiness_score}%</div>
        <div style="font-size:12px; font-weight:600; text-transform:uppercase;">Role Readiness</div>
    </div>
</div>

<div class="section-title">1. Executive Professional Summary</div>
<p style="background:#f8fafc; padding:14px; border-radius:6px; border-left:4px solid #0f172a; font-size:14px; margin-top:8px;">
    {summary.executive_summary}
</p>

<div class="section-title">2. Skill-Gap & Benchmark Analysis</div>
<table>
    <thead>
        <tr>
            <th>Skill Name</th>
            <th>Category</th>
            <th>Status</th>
            <th>Current</th>
            <th>Required</th>
            <th>Impact Rationale</th>
        </tr>
    </thead>
    <tbody>
        {gaps_rows}
    </tbody>
</table>

<div class="section-title">3. Actionable Learning Roadmap ({roadmap.total_weeks} Weeks @ {roadmap.weekly_hours} Hours/Week)</div>
{roadmap_phases_html}

<div class="section-title">4. Core Technical & Project Defense Interview Focus</div>
<div style="font-size:14px; color:#475569; margin-bottom:12px;">
    Key topics prioritized for immediate technical mastery:
</div>
<ul style="font-size:14px; color:#334155; line-height:1.7;">
    {"".join(f"<li><strong>{q.topic}:</strong> {q.question}</li>" for q in interview_prep.technical_questions[:3])}
    {"".join(f"<li><strong>Architecture Defense:</strong> {q.question}</li>" for q in interview_prep.project_defense_questions[:2])}
</ul>

</body>
</html>
"""
