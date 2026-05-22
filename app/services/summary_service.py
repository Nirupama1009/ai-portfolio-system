class SummaryService:

    def generate_summary(self, name, role, skills):
        skills_text = ", ".join(skills[:5])  # limit to top 5 skills

        summary = (
            f"{name} is an aspiring {role} with strong foundations in "
            f"{skills_text}. Passionate about applying analytical thinking "
            f"and technical expertise to solve real-world problems. "
            f"Continuously learning and improving to stay aligned with "
            f"industry standards and emerging technologies."
        )

        return summary