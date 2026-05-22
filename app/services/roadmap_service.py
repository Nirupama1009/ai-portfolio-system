"""Roadmap Service

Generates personalized learning roadmaps based on skill gaps.
"""

from typing import List, Dict, Any


class RoadmapService:
    """Generates structured learning roadmaps for skill development."""
    
    def generate_roadmap(self, ranked_missing_skills: List[str]) -> List[Dict[str, str]]:
        """Generate a week-based learning roadmap for missing skills.
        
        Creates a structured learning plan with one skill per week.
        
        Args:
            ranked_missing_skills: List of skills to learn, in priority order.
            
        Returns:
            List of roadmap items with week, focus, and description.
        """
        roadmap: List[Dict[str, str]] = []

        # Lightweight mapping of skills to suggested course titles and platforms
        platform_catalog = [
            ("Coursera", "https://www.coursera.org"),
            ("edX", "https://www.edx.org"),
            ("freeCodeCamp", "https://www.freecodecamp.org"),
            ("Udemy", "https://www.udemy.com"),
            ("Khan Academy", "https://www.khanacademy.org")
        ]

        for week_num, skill in enumerate(ranked_missing_skills, start=1):
            title = f"Intro to {skill.capitalize()}"
            # Rotate platforms to give variety
            platform, link = platform_catalog[(week_num - 1) % len(platform_catalog)]

            roadmap.append({
                "week": f"Week {week_num}",
                "focus": skill.capitalize(),
                "description": f"Learn and practice {skill.capitalize()} through tutorials and hands-on exercises.",
                "course": title,
                "platform": platform,
                "link": link
            })

        return roadmap