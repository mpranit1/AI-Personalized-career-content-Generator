import uuid
from typing import List, Dict, Any, Optional

from backend.models.student import StudentProfile
from backend.models.career_data import RoleBenchmark, RoleSkillRequirement
from backend.models.dossier import (
    ProfessionalSummary,
    SkillGapReport,
    SkillGapItem,
    GapStatus,
    GapSeverity,
    LearningRoadmap,
    RoadmapPhase,
    LearningRecommendationItem,
    CuratedResource,
    InterviewPrepPackage,
    InterviewQuestion,
    QuestionCategory,
    StarStoryBreakdown,
)

class ProfileContentGenerator:
    @classmethod
    def generate_professional_summary(
        cls,
        profile: StudentProfile,
        benchmark: RoleBenchmark,
        gap_report: SkillGapReport
    ) -> ProfessionalSummary:
        edu = profile.education
        target_role = benchmark.canonical_title
        
        # Extract strongest skills
        matched_or_advanced = [
            s.name for s in profile.skills 
            if s.proficiency.value in ("intermediate", "advanced", "expert")
        ][:5]
        skills_str = ", ".join(matched_or_advanced) if matched_or_advanced else "Python, problem-solving, and software engineering"

        # Projects summary
        top_projects = profile.projects[:2]
        project_mention = ""
        if top_projects:
            p = top_projects[0]
            project_mention = f" Demonstrated practical application through building {p.title}"
            if p.tech_stack:
                project_mention += f" using {', '.join(p.tech_stack[:3])}"
            project_mention += "."

        # Academic interests highlight
        interest_str = ""
        if profile.academic_interests:
            interest_str = f" with focused academic and research curiosity in {', '.join(profile.academic_interests[:2])}"

        # 1. Headline
        headline = f"Aspiring {target_role} | {edu.degree} in {edu.major} @ {edu.institution} | {skills_str.split(',')[0]} & Systems"
        alt_headlines = [
            f"{target_role} Candidate | {edu.major} Graduate | Passionate about {' & '.join(profile.academic_interests[:2]) if profile.academic_interests else 'Scalable Systems'}",
            f"{edu.major} Scholar @ {edu.institution} | Building Production-Grade Solutions in {target_role}",
            f"Software & {target_role} Enthusiast | Proficient in {skills_str}",
        ]

        # 2. Executive Summary
        exec_summary = (
            f"Results-driven {edu.degree} in {edu.major} candidate at {edu.institution} (Class of {edu.graduation_year})"
            f"{interest_str}, targeting {target_role} opportunities. Combines rigorous theoretical foundations with "
            f"hands-on engineering experience in {skills_str}.{project_mention} "
            f"Proven aptitude for rapid technical acquisition, reproducible development practices, and cross-functional collaboration."
        )

        # 3. LinkedIn About Section
        key_courses_txt = f" My coursework in {', '.join(edu.coursework[:4])} provided deep grounding in computational fundamentals." if edu.coursework else ""
        
        project_details_txt = ""
        if profile.projects:
            project_details_txt = "\n\nKey Practical Highlights:\n"
            for prj in profile.projects[:2]:
                stack = f" ({', '.join(prj.tech_stack)})" if prj.tech_stack else ""
                hl = f" - {prj.highlights[0]}" if prj.highlights else ""
                project_details_txt += f"• {prj.title}{stack}: {prj.description}{hl}\n"

        linkedin_about = (
            f"I am a passionate software and data practitioner completing my {edu.degree} in {edu.major} at {edu.institution}, "
            f"specializing in {target_role} workflows.{key_courses_txt}\n\n"
            f"My technical toolbox centers around {skills_str}. I thrive at the intersection of theory and practical implementation—transforming "
            f"complex algorithms and system architectures into robust, production-ready code.{project_details_txt}\n"
            f"Currently gearing up for entry-level / junior {target_role} roles where I can deliver immediate engineering impact while learning from world-class teams.\n\n"
            f"Let's connect: {profile.email} | Open to collaborative projects and opportunities!"
        )

        # 4. 30-Second Elevator Pitch
        first_interest = profile.academic_interests[0] if profile.academic_interests else "technology and data"
        elevator_pitch = (
            f"Hi! I'm {profile.name}, finishing my {edu.degree} in {edu.major} at {edu.institution}. "
            f"I specialize in {skills_str.split(',')[0]} and practical engineering for {target_role} positions, with a deep interest in {first_interest}. "
            f"Recently, I built {top_projects[0].title if top_projects else 'several end-to-end technical projects'} "
            f"which tackled real-world performance challenges. I'm actively looking for junior {target_role} roles where I can build impactful, resilient software."
        )

        # 5. Key Value Propositions
        val_props = [
            f"Strong Theoretical & Academic Backbone: Rigorous training in {edu.major} at {edu.institution} with high-caliber problem solving.",
            f"Hands-On Project Portfolio: Demonstrated ability to deliver end-to-end applications beyond classroom toy assignments.",
            f"Proactive Gap Closure: Actively pursuing a targeted upskilling roadmap addressing {', '.join(gap_report.top_priority_gaps[:3]) if gap_report.top_priority_gaps else 'industry standards'}.",
            f"Domain Passion: Focused curiosity in {', '.join(profile.academic_interests) if profile.academic_interests else target_role} ensuring high self-motivation."
        ]

        core_comp = list(dict.fromkeys([s.name for s in profile.skills[:6]] + [req.name for req in benchmark.skills[:4]]))

        return ProfessionalSummary(
            target_role=target_role,
            headline=headline,
            alternative_headlines=alt_headlines,
            executive_summary=exec_summary,
            linkedin_about=linkedin_about,
            elevator_pitch_30s=elevator_pitch,
            key_value_propositions=val_props,
            core_competencies=core_comp,
        )

    @classmethod
    def generate_learning_roadmap(
        cls,
        profile: StudentProfile,
        benchmark: RoleBenchmark,
        gap_report: SkillGapReport
    ) -> LearningRoadmap:
        weekly_hours = max(5, profile.hours_per_week_available)
        
        # Benchmark requirements map
        req_lookup: Dict[str, RoleSkillRequirement] = {
            r.name.lower(): r for r in benchmark.skills
        }

        # Filter gaps that need work (Critical, High, Medium, Partial)
        actionable_gaps = [
            g for g in gap_report.gaps 
            if g.status in (GapStatus.MISSING, GapStatus.PARTIAL)
        ]

        if not actionable_gaps:
            # All skills matched, create an advanced specialization phase
            actionable_gaps = [
                SkillGapItem(
                    skill_name="Advanced Production Engineering & Scale",
                    category="Domain & Architecture",
                    status=GapStatus.PARTIAL,
                    required_proficiency="expert",
                    severity=GapSeverity.LOW,
                    impact_analysis="Pushing from intermediate to production mastery.",
                    remediation_priority=1
                )
            ]

        # Partition into phases
        # Phase 1: Critical and High severity gaps
        # Phase 2: Medium severity gaps & hands-on integration
        # Phase 3: Capstone, portfolio packaging, and mock testing
        phase1_items: List[LearningRecommendationItem] = []
        phase2_items: List[LearningRecommendationItem] = []
        phase3_items: List[LearningRecommendationItem] = []

        for idx, gap in enumerate(actionable_gaps, 1):
            req_info = req_lookup.get(gap.skill_name.lower())
            
            resources: List[CuratedResource] = []
            if req_info and req_info.learning_resources:
                for r in req_info.learning_resources:
                    resources.append(
                        CuratedResource(
                            title=r["title"],
                            resource_type=r.get("resource_type", "Course"),
                            url_or_platform=r.get("url_or_platform", "Online Resource"),
                            estimated_hours=r.get("estimated_hours", 15),
                            difficulty=r.get("difficulty", "Intermediate"),
                        )
                    )
            else:
                resources = [
                    CuratedResource(
                        title=f"Industry Best Practices & Fundamentals for {gap.skill_name}",
                        resource_type="Documentation & Practical Labs",
                        url_or_platform=f"Official {gap.skill_name} Docs & Interactive Tutorials",
                        estimated_hours=16,
                        difficulty="Intermediate"
                    )
                ]

            capstone = (
                req_info.recommended_capstone_task 
                if (req_info and req_info.recommended_capstone_task) 
                else f"Develop a modular, tested reference module demonstrating {gap.skill_name} in an end-to-end pipeline."
            )
            
            deliverable = f"Open-source GitHub repo with README, unit test suite, and CI/CD demonstration for {gap.skill_name}."

            rec = LearningRecommendationItem(
                gap_skill=gap.skill_name,
                category=gap.category,
                severity=gap.severity,
                priority_order=idx,
                target_proficiency=gap.required_proficiency,
                recommended_action=f"Bridge from current status ({gap.status.value}) to {gap.required_proficiency} via structured practical labs.",
                curated_resources=resources,
                capstone_mini_project=capstone,
                verification_deliverable=deliverable,
                estimated_weeks=max(2, round(25 / weekly_hours)),
            )

            if gap.severity in (GapSeverity.CRITICAL, GapSeverity.HIGH):
                phase1_items.append(rec)
            elif gap.severity == GapSeverity.MEDIUM:
                phase2_items.append(rec)
            else:
                phase3_items.append(rec)

        # Ensure no phase is completely empty
        if not phase1_items and phase2_items:
            phase1_items.append(phase2_items.pop(0))
        if not phase2_items and phase1_items and len(phase1_items) > 1:
            phase2_items.append(phase1_items.pop())

        # Construct Phases
        phases: List[RoadmapPhase] = []
        p1_weeks = max(3, sum(r.estimated_weeks for r in phase1_items) // max(1, len(phase1_items)))
        phases.append(
            RoadmapPhase(
                phase_number=1,
                phase_name="Core Foundation & Critical Skill Remediation",
                duration_weeks=p1_weeks,
                focus_summary=f"Eliminate must-have role blockers ({', '.join(r.gap_skill for r in phase1_items)}).",
                recommendations=phase1_items,
            )
        )

        p2_weeks = max(3, sum(r.estimated_weeks for r in phase2_items) // max(1, len(phase2_items))) if phase2_items else 3
        phases.append(
            RoadmapPhase(
                phase_number=2,
                phase_name="System Integration, Tools & Scalability",
                duration_weeks=p2_weeks,
                focus_summary="Deepen tooling, infrastructure, and real-world edge case handling.",
                recommendations=phase2_items or phase1_items[:1],
            )
        )

        # Capstone phase
        target_role = benchmark.canonical_title
        p3_rec = LearningRecommendationItem(
            gap_skill=f"{target_role} Portfolio Capstone",
            category="Domain & Architecture",
            severity=GapSeverity.LOW,
            priority_order=99,
            target_proficiency="advanced",
            recommended_action=f"Synthesize all skills into a signature production-ready capstone project for {target_role}.",
            curated_resources=[
                CuratedResource(
                    title="Clean Code & Production Architecture Standards",
                    resource_type="Book",
                    url_or_platform="Martin Fowler / O'Reilly",
                    estimated_hours=15,
                    difficulty="Advanced"
                )
            ],
            capstone_mini_project=f"Build and deploy a full-lifecycle {target_role} application with live endpoint, automated evaluation, Docker containerization, and monitoring.",
            verification_deliverable="Public live URL, documented API docs, and comprehensive architecture diagram.",
            estimated_weeks=3,
        )
        phases.append(
            RoadmapPhase(
                phase_number=3,
                phase_name="Signature Portfolio Capstone & Technical Interview Hardening",
                duration_weeks=3,
                focus_summary="Complete an end-to-end capstone deliverable and conduct timed coding & system design simulations.",
                recommendations=[p3_rec],
            )
        )

        total_weeks = sum(p.duration_weeks for p in phases)
        total_hours = total_weeks * weekly_hours

        milestones = [
            f"End of Week {phases[0].duration_weeks}: Complete critical gap projects and pass automated tests.",
            f"End of Week {phases[0].duration_weeks + phases[1].duration_weeks}: Deploy containerized microservice with logging and monitoring.",
            f"End of Week {total_weeks}: Finalize public portfolio GitHub repos, resume update, and execute 3 mock interviews."
        ]

        return LearningRoadmap(
            target_role=benchmark.canonical_title,
            total_weeks=total_weeks,
            weekly_hours=weekly_hours,
            total_study_hours=total_hours,
            phases=phases,
            suggested_certifications=benchmark.certifications,
            milestone_deliverables=milestones,
        )

    @classmethod
    def generate_interview_prep(
        cls,
        profile: StudentProfile,
        benchmark: RoleBenchmark,
        gap_report: SkillGapReport
    ) -> InterviewPrepPackage:
        technical_questions: List[InterviewQuestion] = []
        behavioral_questions: List[InterviewQuestion] = []
        project_defense_questions: List[InterviewQuestion] = []

        # 1. Technical Questions from benchmark skills
        for idx, req in enumerate(benchmark.skills[:4], 1):
            q_data = req.interview_question
            technical_questions.append(
                InterviewQuestion(
                    id=f"tech-{idx}",
                    category=QuestionCategory.TECHNICAL,
                    topic=q_data.get("topic", req.name),
                    question=q_data.get("question", f"Explain core concepts and architectural best practices of {req.name}."),
                    context_or_scenario=f"Commonly asked in technical screening rounds for {benchmark.canonical_title}.",
                    sample_ideal_answer=q_data.get("sample_ideal_answer", f"A strong answer outlines fundamental architecture, state management, and real-world performance trade-offs in {req.name}."),
                    key_concepts_to_demonstrate=q_data.get("key_concepts", [req.name, "Trade-offs", "Complexity"]),
                    pitfalls_to_avoid=q_data.get("pitfalls", ["Surface-level definitions without understanding runtime mechanisms"]),
                )
            )

        # 2. Behavioral Questions (STAR Method) tailored to Student's Experience
        edu = profile.education
        first_project = profile.projects[0] if profile.projects else None
        p_name = first_project.title if first_project else "an intensive academic team capstone"

        behavioral_questions.append(
            InterviewQuestion(
                id="beh-1",
                category=QuestionCategory.BEHAVIORAL_STAR,
                topic="Overcoming Unexpected Technical Roadblocks",
                question=f"Tell me about a time during {p_name} when you encountered a severe technical roadblock or bug. How did you diagnose and resolve it?",
                context_or_scenario="Evaluates debugging methodology, persistence, and problem decomposition under pressure.",
                sample_ideal_answer=(
                    f"In {p_name}, we hit a severe performance bottleneck during system integration. "
                    f"Instead of blindly altering parameters, I isolated components using profiling logs, identified the root cause in data serialization, "
                    f"and refactored the pipeline to use vectorized streaming, successfully recovering expected latency."
                ),
                key_concepts_to_demonstrate=["Root Cause Analysis", "Systematic Profiling", "Resilience", "Data-Driven Decisions"],
                pitfalls_to_avoid=["Blaming teammate mistakes", "Describing a bug fix without explaining why it happened"],
                star_breakdown=StarStoryBreakdown(
                    situation=f"Developing {p_name} while managing academic deadlines at {edu.institution}.",
                    task="Ensure the application met performance latency and throughput thresholds for production testing.",
                    action="Profiled memory and CPU usage, hypothesized root causes, wrote benchmark unit tests, and refactored the bottleneck.",
                    result=f"Achieved stable performance, verified through automated tests, and delivered the project on schedule."
                ),
                referenced_student_project=p_name
            )
        )

        behavioral_questions.append(
            InterviewQuestion(
                id="beh-2",
                category=QuestionCategory.BEHAVIORAL_STAR,
                topic="Rapid Learning of Unfamiliar Technologies",
                question=f"As an aspiring {benchmark.canonical_title}, you will frequently encounter new frameworks. Describe how you quickly master unfamiliar tools.",
                context_or_scenario="Evaluates autonomy, speed of learning, and engineering resourcefulness.",
                sample_ideal_answer=(
                    "When learning a new tool, I follow a three-step protocol: first, read official conceptual documentation to understand the mental model; "
                    "second, build an isolated 'hello world' prototype testing boundaries and failure modes; third, integrate it into a real codebase with tests."
                ),
                key_concepts_to_demonstrate=["Structured Learning Protocols", "Hands-On Prototyping", "Continuous Improvement"],
                pitfalls_to_avoid=["Passive tutorial-watching without writing code"]
            )
        )

        # 3. Project Defense Questions tailored to the student's listed projects
        if profile.projects:
            for idx, prj in enumerate(profile.projects[:2], 1):
                techs = ", ".join(prj.tech_stack) if prj.tech_stack else "the chosen stack"
                project_defense_questions.append(
                    InterviewQuestion(
                        id=f"proj-def-{idx}",
                        category=QuestionCategory.PROJECT_DEFENSE,
                        topic=f"Architecture Defense: {prj.title}",
                        question=f"In your project '{prj.title}', why did you select {techs}? What were the key architectural tradeoffs compared to alternative approaches?",
                        context_or_scenario="Interviewers ask this to distinguish candidates who truly built the system from those who copied templates.",
                        sample_ideal_answer=(
                            f"For '{prj.title}', we prioritized rapid iteration, type safety, and low operational overhead. "
                            f"While alternatives offered established ecosystems, our chosen stack ({techs}) provided better ergonomics for our data models. "
                            f"The trade-off was managing fewer third-party integrations, which we addressed by writing clean adapter interfaces."
                        ),
                        key_concepts_to_demonstrate=["Architectural Trade-offs", "Technology Selection Rationales", "Decoupling & Abstractions"],
                        pitfalls_to_avoid=["Saying 'I picked it because it's popular' without technical justification"],
                        referenced_student_project=prj.title
                    )
                )
        else:
            project_defense_questions.append(
                InterviewQuestion(
                    id="proj-def-1",
                    category=QuestionCategory.PROJECT_DEFENSE,
                    topic=f"Academic Coursework Translation",
                    question=f"How does your coursework in {edu.coursework[0] if edu.coursework else edu.major} translate directly to solving problems as a {benchmark.canonical_title}?",
                    sample_ideal_answer="Academic coursework established rigorous theoretical boundaries (complexity theory, invariant proofs) which allows me to avoid naive architectural traps and reason mathematically about system capacity.",
                    key_concepts_to_demonstrate=["Theory to Practice Bridge", "Mathematical Rigor"],
                    pitfalls_to_avoid=["Dismissing academic theory as irrelevant to industry"]
                )
            )

        # 4. Day-Before Cheat Sheet & Red Flags
        first_proj_title = profile.projects[0].title if profile.projects else "capstone"
        cheat_sheet = [
            f"Review your project '{first_proj_title}' line-by-line: be ready to sketch its architecture on a whiteboard.",
            f"Prepare 2 clarifying questions before writing code in coding rounds (e.g. constraints on inputs, memory limits, edge cases like null/empty).",
            f"Memorize Big-O time and space complexities for hash maps, balanced trees, quicksort, and binary search.",
            f"Be ready to articulate your 30-second elevator pitch clearly when asked 'Tell me about yourself'.",
            f"Have 3 thoughtful questions prepared for the interviewer about engineering culture, deployment pipelines, and team roadmaps."
        ]

        red_flags = [
            "Claiming expertise in a skill during conversation that you cannot explain the internal mechanics of.",
            "Jumping straight into coding without asking clarifying questions or validating input constraints.",
            "Speaking negatively about past teammates, professors, or universities during behavioral scenarios.",
            "Pretending to know an unfamiliar acronym rather than asking for clarification."
        ]

        return InterviewPrepPackage(
            target_role=benchmark.canonical_title,
            technical_questions=technical_questions,
            behavioral_questions=behavioral_questions,
            project_defense_questions=project_defense_questions,
            day_before_cheat_sheet=cheat_sheet,
            interviewer_red_flags=red_flags,
        )
