from typing import List, Dict, Any
from fastapi import APIRouter, HTTPException, Response
from fastapi.responses import HTMLResponse, PlainTextResponse

from backend.models.student import StudentProfile
from backend.models.dossier import UnifiedCareerDossier, ConsistencyAuditResult
from backend.models.career_data import ROLE_BENCHMARKS
from backend.services.orchestrator import CareerDossierOrchestrator
from backend.services.consistency import ConsistencyAuditor
from backend.config import config

router = APIRouter()
orchestrator = CareerDossierOrchestrator()

# In-memory presets for instant testing
SAMPLE_PRESETS: Dict[str, Dict[str, Any]] = {
    "cs_ml_junior": {
        "name": "Alex Chen",
        "email": "alex.chen@berkeley.edu",
        "location": "Berkeley, CA",
        "education": {
            "institution": "University of California, Berkeley",
            "degree": "B.S.",
            "major": "Computer Science",
            "graduation_year": 2026,
            "gpa": "3.85 / 4.0",
            "coursework": [
                "CS 189: Introduction to Machine Learning",
                "CS 61B: Data Structures & Algorithms",
                "CS 162: Operating Systems",
                "EECS 127: Optimization Models"
            ],
            "honors": ["Dean's Honors List (3 terms)", "Regents Scholar"]
        },
        "skills": [
            {"name": "Python", "proficiency": "advanced", "category": "Programming & Languages", "years_experience": 3.0},
            {"name": "PyTorch", "proficiency": "intermediate", "category": "Data Science & Machine Learning", "years_experience": 1.5},
            {"name": "SQL", "proficiency": "intermediate", "category": "Databases & Storage", "years_experience": 1.0},
            {"name": "Git", "proficiency": "intermediate", "category": "Developer Tools & CI/CD", "years_experience": 2.0},
            {"name": "C++", "proficiency": "intermediate", "category": "Programming & Languages", "years_experience": 1.5},
            {"name": "Scikit-Learn", "proficiency": "intermediate", "category": "Data Science & Machine Learning", "years_experience": 1.0}
        ],
        "academic_interests": ["Deep Learning & Computer Vision", "Efficient Model Inference", "High-Performance Systems"],
        "career_goal": {
            "target_role": "Junior Machine Learning Engineer",
            "seniority_level": "Entry-Level / Junior (0-2 YOE)",
            "target_industry": "AI & Autonomous Systems",
            "timeline_months": 6,
            "preferred_work_style": "Hybrid"
        },
        "projects": [
            {
                "title": "EdgeVision: Low-Latency Object Detection",
                "description": "Quantized and pruned a YOLOv8 model for real-time edge inference on Jetson Nano.",
                "role": "Lead ML Developer",
                "tech_stack": ["Python", "PyTorch", "TensorRT", "OpenCV"],
                "highlights": [
                    "Achieved 2.8x inference speedup with under 1.2% mAP degradation",
                    "Integrated real-time webcam streaming benchmark"
                ],
                "link": "https://github.com/alexchen/edge-vision"
            },
            {
                "title": "Distributed Key-Value Store",
                "description": "Implemented a Raft-consensus distributed replicated key-value storage engine in C++.",
                "role": "Systems Engineer",
                "tech_stack": ["C++", "gRPC", "CMake", "POSIX Sockets"],
                "highlights": [
                    "Passed 100% linearizability stress tests under simulated network partitions",
                    "Handled 12,000 requests/sec across 5-node cluster"
                ],
                "link": "https://github.com/alexchen/raft-kv"
            }
        ],
        "hours_per_week_available": 12,
        "learning_style": "project_based",
        "existing_certifications": [],
        "bio_notes": "Passionate about bridging modern deep learning research to scalable production infrastructure."
    },
    "data_science_ms": {
        "name": "Maya Patel",
        "email": "mpatel@columbia.edu",
        "location": "New York, NY",
        "education": {
            "institution": "Columbia University",
            "degree": "M.S.",
            "major": "Data Science",
            "graduation_year": 2026,
            "gpa": "3.92 / 4.0",
            "coursework": [
                "Statistical Inference & Modeling",
                "Machine Learning for Data Science",
                "Exploratory Data Analysis & Visualization",
                "Applied Deep Learning"
            ],
            "honors": ["Columbia Engineering Fellowship"]
        },
        "skills": [
            {"name": "Python", "proficiency": "advanced", "category": "Programming & Languages", "years_experience": 3.0},
            {"name": "SQL", "proficiency": "advanced", "category": "Databases & Storage", "years_experience": 2.5},
            {"name": "Pandas", "proficiency": "advanced", "category": "Data Science & Machine Learning", "years_experience": 2.5},
            {"name": "Scikit-Learn", "proficiency": "intermediate", "category": "Data Science & Machine Learning", "years_experience": 2.0},
            {"name": "R", "proficiency": "intermediate", "category": "Programming & Languages", "years_experience": 1.5},
            {"name": "Tableau", "proficiency": "intermediate", "category": "Other", "years_experience": 1.0}
        ],
        "academic_interests": ["Causal Inference", "FinTech Predictive Modeling", "Experimentation & A/B Testing"],
        "career_goal": {
            "target_role": "Data Scientist",
            "seniority_level": "Associate / Entry-Level",
            "target_industry": "FinTech / SaaS",
            "timeline_months": 4,
            "preferred_work_style": "Remote"
        },
        "projects": [
            {
                "title": "Customer Churn Prediction & Survival Analysis",
                "description": "Formulated a Cox proportional hazards model and Gradient Boosted Trees to identify customer churn risk factors.",
                "role": "Data Scientist",
                "tech_stack": ["Python", "Lifelines", "XGBoost", "PostgreSQL"],
                "highlights": [
                    "Identified 3 leading early churn indicators driving 80% of customer drop-off",
                    "Produced interactive executive dashboard communicating financial impact"
                ],
                "link": "https://github.com/mayapatel/churn-survival"
            }
        ],
        "hours_per_week_available": 15,
        "learning_style": "project_based",
        "existing_certifications": ["IBM Data Science Professional Certificate"]
    },
    "bootcamp_fullstack": {
        "name": "Jordan Rivera",
        "email": "jordan.rivera@example.com",
        "location": "Austin, TX",
        "education": {
            "institution": "University of Texas, Austin",
            "degree": "B.A.",
            "major": "Economics & Information Systems",
            "graduation_year": 2025,
            "gpa": "3.6 / 4.0",
            "coursework": [
                "Full-Stack Web Engineering",
                "Database Management Systems",
                "Software Design Principles"
            ],
            "honors": []
        },
        "skills": [
            {"name": "JavaScript", "proficiency": "intermediate", "category": "Programming & Languages", "years_experience": 1.5},
            {"name": "React", "proficiency": "intermediate", "category": "Web & Frontend", "years_experience": 1.0},
            {"name": "HTML & CSS", "proficiency": "advanced", "category": "Web & Frontend", "years_experience": 2.0},
            {"name": "Git", "proficiency": "intermediate", "category": "Developer Tools & CI/CD", "years_experience": 1.5},
            {"name": "SQL", "proficiency": "beginner", "category": "Databases & Storage", "years_experience": 0.5}
        ],
        "academic_interests": ["Responsive Web Applications", "Interactive Visualizations", "FinTech Dashboards"],
        "career_goal": {
            "target_role": "Full Stack Web Developer",
            "seniority_level": "Junior (0-1 YOE)",
            "target_industry": "E-Commerce / Consumer Tech",
            "timeline_months": 3,
            "preferred_work_style": "Hybrid"
        },
        "projects": [
            {
                "title": "ShopEase: Responsive E-Commerce Platform",
                "description": "Full-stack e-commerce store with product search, cart state management, and checkout.",
                "role": "Frontend Developer",
                "tech_stack": ["React", "JavaScript", "Tailwind CSS", "Stripe API"],
                "highlights": [
                    "Implemented responsive UI scoring 98 on Google Lighthouse",
                    "Integrated secure client-side payment processing"
                ],
                "link": "https://github.com/jordanrivera/shopease"
            }
        ],
        "hours_per_week_available": 20,
        "learning_style": "project_based"
    }
}

@router.get("/health")
def get_health():
    return {
        "status": "healthy",
        "app_name": config.app_name,
        "version": config.version,
        "llm_available": orchestrator.llm_provider.is_available(),
        "model": orchestrator.llm_provider.model_name if orchestrator.llm_provider.is_available() else "Knowledge Graph Engine"
    }

@router.get("/roles")
def get_benchmark_roles():
    """List available benchmark roles and their metadata."""
    roles_list = []
    for k, v in ROLE_BENCHMARKS.items():
        roles_list.append({
            "key": k,
            "title": v.canonical_title,
            "seniority": v.standard_seniority,
            "description": v.description,
            "skills_count": len(v.skills),
            "certifications": v.certifications,
        })
    return {"roles": roles_list}

@router.get("/presets")
def get_presets():
    """Returns sample pre-filled profiles for easy demonstration."""
    return {"presets": SAMPLE_PRESETS}

@router.post("/generate", response_model=UnifiedCareerDossier)
def generate_career_dossier(profile: StudentProfile):
    """
    Main endpoint: Generates complete personalized career dossier:
    - Professional summary
    - Skill gap report
    - Phased learning roadmap
    - Role-specific interview prep
    - Formatted exports (Resume, LinkedIn, HTML, Study Guide)
    - Cross-format consistency audit
    """
    try:
        dossier = orchestrator.generate_dossier(profile)
        return dossier
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Generation error: {str(e)}")

@router.post("/export/resume")
def export_markdown_resume(profile: StudentProfile):
    """Directly returns downloadable markdown resume."""
    dossier = orchestrator.generate_dossier(profile)
    filename = f"{profile.name.replace(' ', '_')}_Resume.md"
    return PlainTextResponse(
        content=dossier.formatted_artifacts.markdown_resume,
        headers={"Content-Disposition": f'attachment; filename="{filename}"'}
    )

@router.post("/export/dossier-html", response_class=HTMLResponse)
def export_html_dossier(profile: StudentProfile):
    """Returns clean, self-contained HTML report ready for printing/PDF saving."""
    dossier = orchestrator.generate_dossier(profile)
    return HTMLResponse(content=dossier.formatted_artifacts.career_dossier_html)

