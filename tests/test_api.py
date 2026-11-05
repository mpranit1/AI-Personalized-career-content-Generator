import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "version" in data

def test_roles_endpoint():
    response = client.get("/api/v1/roles")
    assert response.status_code == 200
    data = response.json()
    assert "roles" in data
    assert len(data["roles"]) > 0

def test_presets_endpoint():
    response = client.get("/api/v1/presets")
    assert response.status_code == 200
    data = response.json()
    assert "presets" in data
    assert "cs_ml_junior" in data["presets"]

def test_generate_endpoint_success():
    payload = {
        "name": "Sarah Connor",
        "email": "sarah@future.io",
        "education": {
            "institution": "Caltech",
            "degree": "B.S.",
            "major": "Computer Science",
            "graduation_year": 2026,
            "coursework": ["Robotics", "Control Systems"]
        },
        "skills": [
            {"name": "Python", "proficiency": "advanced", "category": "Programming & Languages"},
            {"name": "PyTorch", "proficiency": "intermediate", "category": "Data Science & Machine Learning"},
            {"name": "Git", "proficiency": "intermediate", "category": "Developer Tools & CI/CD"}
        ],
        "career_goal": {
            "target_role": "Junior Machine Learning Engineer",
            "seniority_level": "Entry-Level",
            "timeline_months": 6
        },
        "projects": [
            {
                "title": "Autonomous Drone Perception",
                "description": "Object recognition on embedded edge GPU.",
                "tech_stack": ["Python", "PyTorch", "ROS"]
            }
        ],
        "hours_per_week_available": 10
    }

    response = client.post("/api/v1/generate", json=payload)
    assert response.status_code == 200
    data = response.json()

    assert "id" in data
    assert "professional_summary" in data
    assert "skill_gap_report" in data
    assert "learning_roadmap" in data
    assert "interview_prep" in data
    assert "consistency_audit" in data
    assert "formatted_artifacts" in data

    # Verify consistency audit score exists and is high
    assert data["consistency_audit"]["overall_consistency_score"] >= 85.0
    assert data["consistency_audit"]["is_consistent"] is True

def test_export_resume_endpoint():
    payload = {
        "name": "David Miller",
        "education": {
            "institution": "UT Austin",
            "degree": "B.S.",
            "major": "CS",
            "graduation_year": 2025
        },
        "skills": [{"name": "Python", "proficiency": "intermediate"}],
        "career_goal": {"target_role": "Backend Software Engineer"}
    }
    response = client.post("/api/v1/export/resume", json=payload)
    assert response.status_code == 200
    assert "David Miller" in response.text
    assert "PROFESSIONAL SUMMARY" in response.text

