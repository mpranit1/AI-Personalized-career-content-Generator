import re
from typing import Dict, Optional, Tuple
from backend.models.career_data import (
    ROLE_BENCHMARKS,
    SKILL_SYNONYMS,
    RoleBenchmark,
    RoleSkillRequirement,
)
from backend.models.student import SkillProficiency

PROFICIENCY_LEVELS = {
    SkillProficiency.BEGINNER.value: 1,
    SkillProficiency.INTERMEDIATE.value: 2,
    SkillProficiency.ADVANCED.value: 3,
    SkillProficiency.EXPERT.value: 4,
}

class TaxonomyService:
    @staticmethod
    def normalize_skill_name(raw_name: str) -> str:
        clean = raw_name.strip()
        lower = clean.lower()
        # Direct dictionary synonym lookup
        if lower in SKILL_SYNONYMS:
            return SKILL_SYNONYMS[lower]
        # Punctuation/version stripped lookup (e.g., 'python 3' -> 'Python')
        cleaned_simple = re.sub(r'[\d\.\-_]+$', '', lower).strip()
        if cleaned_simple in SKILL_SYNONYMS:
            return SKILL_SYNONYMS[cleaned_simple]
        return clean

    @staticmethod
    def get_proficiency_rank(proficiency_str: str) -> int:
        clean = (proficiency_str or "").strip().lower()
        return PROFICIENCY_LEVELS.get(clean, 2)

    @classmethod
    def get_or_synthesize_benchmark(cls, target_role: str, academic_interests: Optional[list] = None) -> RoleBenchmark:
        clean_role = target_role.strip().lower()

        # 1. Exact or partial match in registered role benchmarks
        for key, benchmark in ROLE_BENCHMARKS.items():
            if key in clean_role or clean_role in key:
                return benchmark

        # 2. Keyword-based matching
        if any(w in clean_role for w in ["machine learning", "ml", "ai engineer", "deep learning", "nlp", "computer vision"]):
            base = ROLE_BENCHMARKS["junior machine learning engineer"]
            return cls._adapt_benchmark(base, target_role)
        elif any(w in clean_role for w in ["data science", "data scientist", "analytics", "statistic"]):
            base = ROLE_BENCHMARKS["data scientist"]
            return cls._adapt_benchmark(base, target_role)
        elif any(w in clean_role for w in ["full stack", "fullstack", "web developer", "frontend"]):
            base = ROLE_BENCHMARKS["full stack web developer"]
            return cls._adapt_benchmark(base, target_role)
        elif any(w in clean_role for w in ["devops", "cloud", "sre", "infrastructure"]):
            base = ROLE_BENCHMARKS["cloud & devops engineer"]
            return cls._adapt_benchmark(base, target_role)
        elif any(w in clean_role for w in ["backend", "software engineer", "systems", "api"]):
            base = ROLE_BENCHMARKS["backend software engineer"]
            return cls._adapt_benchmark(base, target_role)

        # 3. Dynamic synthesis for arbitrary custom roles
        return cls._synthesize_custom_benchmark(target_role, academic_interests or [])

    @staticmethod
    def _adapt_benchmark(base: RoleBenchmark, custom_title: str) -> RoleBenchmark:
        return RoleBenchmark(
            role_name=custom_title.lower(),
            canonical_title=custom_title.title(),
            description=f"Personalized benchmark for {custom_title}, adapted from {base.canonical_title} standards.",
            standard_seniority=base.standard_seniority,
            key_responsibilities=base.key_responsibilities,
            industry_keywords=base.industry_keywords,
            skills=base.skills,
            certifications=base.certifications,
        )

    @classmethod
    def _synthesize_custom_benchmark(cls, role_title: str, interests: list) -> RoleBenchmark:
        # Fallback benchmark synthesizing universal software & domain skills
        synthesized_skills = [
            RoleSkillRequirement(
                name="Python",
                category="Programming & Languages",
                required_proficiency="intermediate",
                importance="critical",
                weight=3.0,
                impact_rationale="Core language for algorithmic problem-solving and rapid prototyping.",
                learning_resources=[{"title": "Automate the Boring Stuff with Python", "resource_type": "Book", "url_or_platform": "No Starch Press", "estimated_hours": 20, "difficulty": "Beginner"}],
                recommended_capstone_task="Build an automated data collection and transformation pipeline.",
                interview_question={
                    "topic": "Python Core Concepts",
                    "question": f"How would you architect a maintainable Python solution for {role_title} workloads?",
                    "sample_ideal_answer": "By adopting clean architecture: modularizing concerns, using type hints, enforcing configuration validation via Pydantic, and writing automated unit tests.",
                    "key_concepts": ["Clean Architecture", "Type Hints", "Modularity", "Unit Testing"],
                    "pitfalls": ["Writing monolithic scripts without modular boundaries"]
                }
            ),
            RoleSkillRequirement(
                name="Git & Version Control",
                category="Developer Tools & CI/CD",
                required_proficiency="intermediate",
                importance="high",
                weight=2.0,
                impact_rationale="Essential collaborative standard for team workflows and code review.",
                learning_resources=[{"title": "Pro Git Book", "resource_type": "Book", "url_or_platform": "git-scm.com", "estimated_hours": 10, "difficulty": "Intermediate"}],
                recommended_capstone_task="Set up a multi-branch git workflow with feature branching and semantic PR templates.",
                interview_question={
                    "topic": "Git Branching & Rebasing",
                    "question": "What is the key difference between git merge and git rebase, and when would you prefer each?",
                    "sample_ideal_answer": "Git merge creates a non-destructive merge commit preserving exact chronological branch history. Git rebase re-applies feature branch commits on top of the base tip, creating a clean linear history ideal for personal feature branches before PR.",
                    "key_concepts": ["Fast-forward", "Linear History", "Merge Commits", "Rebase vs Merge"],
                    "pitfalls": ["Rebasing shared public branches"]
                }
            ),
            RoleSkillRequirement(
                name="Data Structures & Algorithms",
                category="Programming & Languages",
                required_proficiency="intermediate",
                importance="high",
                weight=2.0,
                impact_rationale="Core technical baseline for problem-solving efficiency.",
                learning_resources=[{"title": "Grokking Algorithms", "resource_type": "Book", "url_or_platform": "Manning", "estimated_hours": 20, "difficulty": "Beginner"}],
                recommended_capstone_task="Optimize an algorithm from O(N^2) to O(N log N) using appropriate data structures.",
                interview_question={
                    "topic": "Computational Complexity",
                    "question": "How do hash maps achieve O(1) average lookup time, and what causes worst-case O(N) performance?",
                    "sample_ideal_answer": "Hash maps use a hash function to map keys to bucket indices. In the worst case where all keys hash to the same bucket (hash collision clustering), lookups degrade to linear O(N) search through linked chains.",
                    "key_concepts": ["Hash Function", "Collision Resolution", "Load Factor", "Separate Chaining"],
                    "pitfalls": ["Assuming hash lookups are strictly O(1) under adversarial collisions"]
                }
            ),
            RoleSkillRequirement(
                name="System Design Fundamentals",
                category="Domain & Architecture",
                required_proficiency="beginner",
                importance="medium",
                weight=1.5,
                impact_rationale="Understanding architecture trade-offs is crucial for junior engineering longevity.",
                learning_resources=[{"title": "System Design Primer", "resource_type": "Course", "url_or_platform": "GitHub Open Source", "estimated_hours": 25, "difficulty": "Intermediate"}],
                recommended_capstone_task="Diagram a high-level architecture addressing scalability, caching, and failover.",
                interview_question={
                    "topic": "Scalability Trade-offs",
                    "question": "Differentiate between vertical and horizontal scaling and their architectural trade-offs.",
                    "sample_ideal_answer": "Vertical scaling upgrades existing node specs (CPU/RAM); it is simple but hits physical hardware ceilings and introduces a single point of failure. Horizontal scaling adds multiple nodes behind a load balancer, providing resilience and unlimited scale at the expense of distributed complexity.",
                    "key_concepts": ["Horizontal vs Vertical Scaling", "Load Balancing", "Single Point of Failure", "State Management"],
                    "pitfalls": ["Ignoring statefulness issues in horizontal scaling"]
                }
            )
        ]

        return RoleBenchmark(
            role_name=role_title.lower(),
            canonical_title=role_title.title(),
            description=f"Synthesized benchmark specifically tailored for {role_title}.",
            standard_seniority="Entry-Level / Junior (0-2 YOE)",
            key_responsibilities=[
                f"Apply academic foundation to solve real-world problems in {role_title}",
                "Collaborate with engineering teams using version control and agile workflows",
                "Design, write, test, and document modular production code"
            ],
            industry_keywords=[role_title, "Python", "Git", "System Design", "Problem Solving"],
            skills=synthesized_skills,
            certifications=["Foundational Professional Certificate in " + role_title],
        )

