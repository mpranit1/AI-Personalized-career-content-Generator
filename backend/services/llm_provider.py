import json
import logging
from typing import Optional, Dict, Any

from backend.config import config
from backend.models.student import StudentProfile
from backend.models.career_data import RoleBenchmark
from backend.models.dossier import ProfessionalSummary, SkillGapReport

logger = logging.getLogger(__name__)

class LLMProvider:
    def __init__(self):
        self.api_key = config.gemini_api_key
        self.model_name = config.default_model
        self.client = None
        if self.api_key:
            try:
                from google import genai
                self.client = genai.Client(api_key=self.api_key)
                logger.info(f"Gemini LLM Provider initialized with model {self.model_name}")
            except Exception as e:
                logger.warning(f"Failed to initialize Gemini Client: {e}. Falling back to knowledge graph engine.")

    def is_available(self) -> bool:
        return self.client is not None

    def polish_summary_with_llm(
        self,
        base_summary: ProfessionalSummary,
        profile: StudentProfile,
        benchmark: RoleBenchmark,
    ) -> ProfessionalSummary:
        """
        Enhances the generated summary using Gemini if available, ensuring tone and fluency.
        Falls back to base_summary on any failure.
        """
        if not self.is_available():
            return base_summary

        try:
            prompt = f"""
You are an expert career strategist and executive resume coach.
Enhance and elevate the following professional career summaries for a student while strictly preserving their true background.

Student Details:
- Name: {profile.name}
- Degree: {profile.education.degree} in {profile.education.major} at {profile.education.institution} (Class of {profile.education.graduation_year})
- Target Role: {benchmark.canonical_title}
- Top Skills: {', '.join(s.name for s in profile.skills[:6])}
- Academic Interests: {', '.join(profile.academic_interests)}
- Top Project: {profile.projects[0].title if profile.projects else 'Academic Projects'}

Draft Content to Polish:
1. Executive Summary: "{base_summary.executive_summary}"
2. LinkedIn About: "{base_summary.linkedin_about}"
3. 30-Second Elevator Pitch: "{base_summary.elevator_pitch_30s}"

Respond ONLY with a valid JSON object matching this schema:
{{
  "executive_summary": "elevated executive summary",
  "linkedin_about": "elevated narrative linkedin about section",
  "elevator_pitch_30s": "conversational elevator pitch",
  "key_value_propositions": ["prop 1", "prop 2", "prop 3", "prop 4"]
}}
"""
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
            )

            text = response.text.strip()
            # Remove markdown fence if present
            if text.startswith("```json"):
                text = text[7:]
            if text.startswith("```"):
                text = text[3:]
            if text.endswith("```"):
                text = text[:-3]
            text = text.strip()

            data = json.loads(text)
            return ProfessionalSummary(
                target_role=base_summary.target_role,
                headline=base_summary.headline,
                alternative_headlines=base_summary.alternative_headlines,
                executive_summary=data.get("executive_summary", base_summary.executive_summary),
                linkedin_about=data.get("linkedin_about", base_summary.linkedin_about),
                elevator_pitch_30s=data.get("elevator_pitch_30s", base_summary.elevator_pitch_30s),
                key_value_propositions=data.get("key_value_propositions", base_summary.key_value_propositions),
                core_competencies=base_summary.core_competencies,
            )
        except Exception as e:
            logger.warning(f"LLM polishing failed: {e}. Using deterministic semantic generator.")
            return base_summary
