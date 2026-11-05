from typing import List, Optional
from enum import Enum
from pydantic import BaseModel, Field, EmailStr

class SkillProficiency(str, Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"

class SkillCategory(str, Enum):
    PROGRAMMING = "Programming & Languages"
    DATA_ML = "Data Science & Machine Learning"
    SYSTEMS_CLOUD = "Cloud & Infrastructure"
    WEB_FRONTEND = "Web & Frontend"
    WEB_BACKEND = "Backend & APIs"
    DATABASES = "Databases & Storage"
    DEV_TOOLS = "Developer Tools & CI/CD"
    DOMAIN_KNOWLEDGE = "Domain & Architecture"
    SOFT_SKILLS = "Soft & Communication Skills"
    OTHER = "Other"

class SkillItem(BaseModel):
    name: str = Field(..., description="Skill name, e.g., 'Python', 'PyTorch', 'Docker'")
    proficiency: SkillProficiency = Field(default=SkillProficiency.INTERMEDIATE)
    category: Optional[SkillCategory] = Field(default=SkillCategory.OTHER)
    years_experience: Optional[float] = Field(default=1.0, ge=0.0)

class Project(BaseModel):
    title: str = Field(..., description="Project name")
    description: str = Field(..., description="Overview of the problem and solution")
    role: Optional[str] = Field(default="Developer", description="Student's role in the project")
    tech_stack: List[str] = Field(default_factory=list, description="Technologies used, e.g. ['FastAPI', 'React', 'PostgreSQL']")
    highlights: List[str] = Field(default_factory=list, description="Key metrics or achievements, e.g. 'Achieved 94% accuracy', 'Reduced latency by 35%'")
    link: Optional[str] = Field(default=None, description="GitHub repo or live demo link")

class Education(BaseModel):
    institution: str = Field(..., description="University or college name")
    degree: str = Field(..., description="e.g. B.S., M.S., B.Tech")
    major: str = Field(..., description="e.g. Computer Science, Data Science, Software Engineering")
    graduation_year: int = Field(..., description="Expected or completed graduation year")
    gpa: Optional[str] = Field(default=None, description="e.g. '3.8/4.0' or '8.9/10'")
    coursework: List[str] = Field(default_factory=list, description="Relevant academic courses")
    honors: List[str] = Field(default_factory=list, description="Scholarships, Dean's List, etc.")

class CareerGoal(BaseModel):
    target_role: str = Field(..., description="Target job title, e.g. 'Junior Machine Learning Engineer', 'Full Stack Developer'")
    seniority_level: str = Field(default="Entry-Level / Junior", description="Target seniority, e.g. Internship, Entry-Level, Associate")
    target_industry: Optional[str] = Field(default="Tech / Software", description="e.g. FinTech, Healthcare AI, Enterprise SaaS")
    timeline_months: int = Field(default=6, description="Target readiness timeline in months")
    preferred_work_style: Optional[str] = Field(default="Hybrid", description="Remote, Hybrid, or On-site")

class LearningStyle(str, Enum):
    PROJECT_BASED = "project_based"
    VIDEO_COURSES = "video_courses"
    DOCUMENTATION = "documentation"
    CERTIFICATION = "certification"
    BLENDED = "blended"

class StudentProfile(BaseModel):
    name: str = Field(..., description="Student full name")
    email: Optional[str] = Field(default="student@example.edu")
    location: Optional[str] = Field(default="San Francisco, CA")
    education: Education
    skills: List[SkillItem] = Field(..., description="List of current skills")
    academic_interests: List[str] = Field(default_factory=list, description="Specific academic or research focus areas")
    career_goal: CareerGoal
    projects: List[Project] = Field(default_factory=list, description="Relevant projects or practical work")
    hours_per_week_available: int = Field(default=10, ge=1, le=80, description="Available study time per week")
    learning_style: LearningStyle = Field(default=LearningStyle.PROJECT_BASED)
    existing_certifications: List[str] = Field(default_factory=list)
    bio_notes: Optional[str] = Field(default=None, description="Any additional context or preferences")
