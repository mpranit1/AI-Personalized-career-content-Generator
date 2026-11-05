import argparse
import json
import sys
from pathlib import Path

from backend.models.student import StudentProfile
from backend.services.orchestrator import CareerDossierOrchestrator

def main():
    parser = argparse.ArgumentParser(
        description="CareerCraft AI CLI: Generate personalized career content and verify cross-format consistency."
    )
    parser.add_argument("--input", "-i", type=str, default="sample_profiles/cs_student_ml.json", help="Path to student profile JSON file")
    parser.add_argument("--output", "-o", type=str, default=None, help="Path to save output JSON dossier")
    parser.add_argument("--export-resume", type=str, default=None, help="Save generated ATS Resume Markdown to file")
    parser.add_argument("--export-html", type=str, default=None, help="Save printable HTML dossier to file")
    parser.add_argument("--export-linkedin", type=str, default=None, help="Save LinkedIn package to file")
    parser.add_argument("--export-interview", type=str, default=None, help="Save interview prep sheet to file")
    parser.add_argument("--audit-only", action="store_true", help="Print only consistency audit report to stdout")

    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: Input profile file not found at {input_path}")
        sys.exit(1)

    try:
        with open(input_path, "r", encoding="utf-8") as f:
            profile_data = json.load(f)
        profile = StudentProfile(**profile_data)
    except Exception as e:
        print(f"Error parsing profile JSON: {e}")
        sys.exit(1)

    print(f"\n⚡ Generating personalized career dossier for {profile.name}...")
    print(f"🎯 Target Role: {profile.career_goal.target_role}")

    orchestrator = CareerDossierOrchestrator()
    dossier = orchestrator.generate_dossier(profile)

    audit = dossier.consistency_audit
    gap = dossier.skill_gap_report

    print("\n" + "="*60)
    print(f"CAREER DOSSIER GENERATION COMPLETE")
    print(f"Engine: {dossier.model_used}")
    print(f"Overall Role Readiness: {gap.overall_readiness_score}% ({gap.readiness_tier})")
    print(f"Cross-Format Consistency Score: {audit.overall_consistency_score}% (Status: {'PASS' if audit.is_consistent else 'WARN'})")
    print("="*60)

    print("\n📊 SKILL-GAP SUMMARY:")
    print(f"  - Matched Skills: {gap.matched_skills_count}")
    print(f"  - Partial/Developing Skills: {gap.partial_skills_count}")
    print(f"  - Critical/High Gaps: {gap.missing_skills_count}")
    print(f"  - Differentiators: {gap.differentiator_skills_count}")
    if gap.top_priority_gaps:
        print(f"  - Priority Remediation Focus: {', '.join(gap.top_priority_gaps)}")

    print("\n🔍 CROSS-FORMAT CONSISTENCY AUDIT CHECKS:")
    for chk in audit.audit_checks:
        status_symbol = "✅" if chk.status.value == "PASS" else ("⚠️" if chk.status.value == "WARN" else "❌")
        print(f"  {status_symbol} [{chk.status.value}] {chk.check_name}: {chk.details}")

    # Exports
    if args.output:
        out_p = Path(args.output)
        out_p.parent.mkdir(parents=True, exist_ok=True)
        with open(out_p, "w", encoding="utf-8") as f:
            f.write(dossier.model_dump_json(indent=2))
        print(f"\n💾 Full JSON dossier saved to: {out_p}")

    if args.export_resume:
        res_p = Path(args.export_resume)
        res_p.parent.mkdir(parents=True, exist_ok=True)
        with open(res_p, "w", encoding="utf-8") as f:
            f.write(dossier.formatted_artifacts.markdown_resume)
        print(f"📄 ATS Resume saved to: {res_p}")

    if args.export_html:
        html_p = Path(args.export_html)
        html_p.parent.mkdir(parents=True, exist_ok=True)
        with open(html_p, "w", encoding="utf-8") as f:
            f.write(dossier.formatted_artifacts.career_dossier_html)
        print(f"🌐 Printable HTML dossier saved to: {html_p}")

    if args.export_linkedin:
        li_p = Path(args.export_linkedin)
        li_p.parent.mkdir(parents=True, exist_ok=True)
        with open(li_p, "w", encoding="utf-8") as f:
            f.write(dossier.formatted_artifacts.linkedin_profile_text)
        print(f"💼 LinkedIn package saved to: {li_p}")

    if args.export_interview:
        int_p = Path(args.export_interview)
        int_p.parent.mkdir(parents=True, exist_ok=True)
        with open(int_p, "w", encoding="utf-8") as f:
            f.write(dossier.formatted_artifacts.interview_study_sheet_markdown)
        print(f"📝 Interview study sheet saved to: {int_p}")

    print("\n✨ Done! Run the interactive web UI using: uvicorn backend.main:app --reload\n")

if __name__ == "__main__":
    main()

