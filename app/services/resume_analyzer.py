"""Resume Analyzer Service

Extracts technical skills from resume text using pattern matching.
"""

import re
from typing import List


class ResumeAnalyzer:
    """Analyzes resume text to extract technical skills."""
    
    def __init__(self) -> None:
        """Initialize with predefined skill keywords."""
        # Basic skill keywords (expandable)
        self.skill_keywords: List[str] = [
            "python",
            "sql",
            "machine learning",
            "data analysis",
            "deep learning",
            "pandas",
            "numpy",
            "scikit-learn",
            "fastapi",
            "power bi",
            "tableau",
            "tensorflow",
            "pytorch",
            "aws",
            "azure",
            "docker",
            "kubernetes",
            "javascript",
            "react",
            "django",
            "git"
        ]

    def extract_skills(self, resume_text: str) -> List[str]:
        """Extract technical skills from resume text.
        
        Args:
            resume_text: The raw resume content to analyze.
            
        Returns:
            List of detected skills (deduplicated).
        """
        if not resume_text:
            return []
            
        normalized_text = resume_text.lower()
        found_skills: List[str] = []

        for skill in self.skill_keywords:
            pattern = r"\b" + re.escape(skill) + r"\b"
            if re.search(pattern, normalized_text):
                found_skills.append(skill)

        return list(set(found_skills))