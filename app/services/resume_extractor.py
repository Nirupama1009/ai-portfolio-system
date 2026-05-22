import re
from typing import Dict, List, Optional


class ResumeExtractor:
    """Extract structured data from resume text"""
    
    def __init__(self, text: str):
        self.text = text
        self.lines = [line.strip() for line in text.split('\n') if line.strip()]
    
    def extract_name(self) -> Optional[str]:
        """Extract name from first meaningful line or email"""
        # Usually the name is at the top
        if len(self.lines) > 0:
            first_line = self.lines[0]
            # Skip if it looks like an email or URL
            if '@' not in first_line and 'http' not in first_line.lower():
                # Remove email-like patterns and URLs
                name = re.sub(r'\b[\w.-]+@[\w.-]+\.\w+\b', '', first_line).strip()
                if name and len(name) > 2:
                    return name
        return None
    
    def extract_email(self) -> Optional[str]:
        """Extract email address from resume"""
        match = re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', self.text)
        return match.group(0) if match else None
    
    def extract_phone(self) -> Optional[str]:
        """Extract phone number"""
        patterns = [
            r'\+?1?\s*\(?[2-9]\d{2}\)?[\s.-]?[2-9]\d{2}[\s.-]?\d{4}',  # US format
            r'\+\d{1,3}[\s.-]?\d{1,4}[\s.-]?\d{1,4}[\s.-]?\d{1,9}',  # International format
            r'\(\d{3}\)\s*\d{3}-\d{4}',  # (555) 555-5555
        ]
        for pattern in patterns:
            match = re.search(pattern, self.text)
            if match:
                return match.group(0).strip()
        return None
    
    def extract_linkedin(self) -> Optional[str]:
        """Extract LinkedIn profile URL"""
        patterns = [
            r'https?://(?:www\.)?linkedin\.com/in/[\w\-/%]+/?',
            r'linkedin\.com/in/[\w\-/%]+/?',
            r'linkedin\.com/pub/[\w\-/%]+/?',
            r'linkedin[:\s]+@?([A-Za-z0-9_.-]+)',
            r'@([A-Za-z0-9_.-]+)\s*$',
        ]

        for pattern in patterns:
            match = re.search(pattern, self.text, re.IGNORECASE | re.MULTILINE)
            if match:
                value = match.group(0).strip()
                value = value.replace('linkedin:', '').strip()
                if value.startswith('@'):
                    value = value[1:].strip()
                if 'linkedin.com' in value.lower():
                    if not value.lower().startswith('http'):
                        value = 'https://' + value.lstrip('/')
                    return value
                # If the resume only has a username, normalize to a profile URL.
                username = match.group(1) if match.lastindex else value
                username = username.strip().strip('/')
                if username:
                    return f'https://www.linkedin.com/in/{username}'
        return None
    
    def extract_github(self) -> Optional[str]:
        """Extract GitHub profile URL"""
        patterns = [
            r'https?://(?:www\.)?github\.com/[\w\-/%]+/?',
            r'github\.com/[\w\-/%]+/?',
            r'github[:\s]+@?([A-Za-z0-9_.-]+)',
            r'@([A-Za-z0-9_.-]+)\s*$',
        ]

        for pattern in patterns:
            match = re.search(pattern, self.text, re.IGNORECASE | re.MULTILINE)
            if match:
                value = match.group(0).strip()
                value = value.replace('github:', '').strip()
                if value.startswith('@'):
                    value = value[1:].strip()
                if 'github.com' in value.lower():
                    if not value.lower().startswith('http'):
                        value = 'https://' + value.lstrip('/')
                    return value
                username = match.group(1) if match.lastindex else value
                username = username.strip().strip('/')
                if username:
                    return f'https://github.com/{username}'
        return None

    def extract_technical_skills(self) -> List[str]:
        """Extract a small list of technical skills from the resume text."""
        skill_keywords = [
            "Python", "SQL", "FastAPI", "Django", "Flask", "Pandas", "NumPy", "Scikit-learn",
            "TensorFlow", "PyTorch", "Machine Learning", "Deep Learning", "Tableau", "Power BI",
            "Docker", "Kubernetes", "AWS", "Azure", "GCP", "JavaScript", "React", "HTML", "CSS",
            "Git", "GitHub", "PostgreSQL", "MySQL", "MongoDB", "NLP", "Data Analysis"
        ]

        normalized_text = self.text.lower()
        found_skills: List[str] = []

        for skill in skill_keywords:
            if skill.lower() in normalized_text:
                found_skills.append(skill)

        # Keep the output compact for form auto-fill.
        unique_skills = []
        seen = set()
        for skill in found_skills:
            skill_key = skill.lower()
            if skill_key not in seen:
                seen.add(skill_key)
                unique_skills.append(skill)

        return unique_skills[:12]

    def extract_soft_skills(self) -> List[str]:
        """Extract common soft skills from the resume text."""
        soft_keywords = [
            'communication', 'leadership', 'teamwork', 'collaboration', 'problem solving',
            'adaptability', 'time management', 'critical thinking', 'creativity', 'presentation',
            'organization', 'mentoring', 'coaching', 'conflict resolution', 'decision making'
        ]

        normalized = self.text.lower()
        found: List[str] = []
        for kw in soft_keywords:
            if kw in normalized:
                # Title-case common multi-word soft skills
                found.append(' '.join([w.capitalize() for w in kw.split()]))

        # Deduplicate while preserving order
        unique = []
        seen = set()
        for s in found:
            key = s.lower()
            if key not in seen:
                seen.add(key)
                unique.append(s)

        return unique[:12]

    def extract_summary(self) -> Optional[str]:
        """Extract a concise summary from an explicit summary/objective section."""
        section_start = None
        section_markers = re.compile(r'^(professional\s+)?summary\b|^objective\b', re.IGNORECASE)
        stop_markers = ('education', 'experience', 'projects', 'skills', 'contact', 'awards', 'certifications')

        for i, line in enumerate(self.lines):
            line_lower = line.lower().strip()
            if section_markers.match(line_lower):
                section_start = i + 1
                break

        if section_start is not None:
            summary_lines = []
            for line in self.lines[section_start:]:
                line_lower = line.lower().strip()
                if any(line_lower == marker or line_lower.startswith(f"{marker}:") or line_lower.startswith(f"{marker} ") for marker in stop_markers):
                    break
                if line and not line.endswith(':'):
                    summary_lines.append(line)
            if summary_lines:
                return ' '.join(summary_lines[:2]).strip()

        # Fallback: use the first meaningful non-contact line near the top.
        for line in self.lines[:8]:
            line_lower = line.lower().strip()
            if len(line) < 20:
                continue
            if any(marker in line_lower for marker in ('@', 'http', 'linkedin', 'github', 'phone', 'email')):
                continue
            if line_lower in ('education', 'experience', 'projects', 'skills'):
                continue
            return line

        return None
    
    def extract_education(self) -> Dict[str, Optional[str]]:
        """Extract education (college and school)"""
        education = {"college": None, "school": None}
        
        in_education_section = False
        major_section_pattern = re.compile(r'^(professional\s+experience|experience|projects|skills|contact|awards|certifications)\b', re.IGNORECASE)
        college_label_pattern = re.compile(r'^(college|university)\b[:\-]?\s*$', re.IGNORECASE)
        school_label_pattern = re.compile(r'^(school|high school|hsc|sslc)\b[:\-]?\s*$', re.IGNORECASE)

        def collect_education_block(start_index: int) -> List[str]:
            parts: List[str] = []
            title_line = self.lines[start_index].strip()
            if title_line and not title_line.endswith(':'):
                parts.append(title_line)
            for j in range(start_index + 1, min(start_index + 5, len(self.lines))):
                next_line = self.lines[j].strip()
                next_line_lower = next_line.lower().strip()
                if major_section_pattern.match(next_line_lower):
                    break
                if next_line.endswith(':'):
                    break
                if college_label_pattern.match(next_line_lower) or school_label_pattern.match(next_line_lower):
                    break
                if next_line:
                    parts.append(next_line)
            return parts

        def append_education_value(current_value: Optional[str], block: List[str]) -> Optional[str]:
            block_text = ', '.join(block).strip()
            if not block_text:
                return current_value
            if not current_value:
                return block_text
            if block_text.lower() in current_value.lower():
                return current_value
            return f"{current_value} | {block_text}"
        
        for i, line in enumerate(self.lines):
            line_lower = line.lower().strip()
            
            # Enter education section
            if line_lower.startswith('education'):
                in_education_section = True
                continue
            
            # Exit education section
            if in_education_section and major_section_pattern.match(line_lower):
                break
            
            # Extract college/university
            if in_education_section and ('college' in line_lower or 'university' in line_lower or college_label_pattern.match(line_lower)):
                college_parts = collect_education_block(i)
                education["college"] = append_education_value(education["college"], college_parts)
            
            # Extract school / HSC / SSLC entries
            if in_education_section and (school_label_pattern.match(line_lower) or 'high school' in line_lower or 'hsc' in line_lower or 'sslc' in line_lower):
                school_parts = collect_education_block(i)
                education["school"] = append_education_value(education["school"], school_parts)
        
        return education
    
    def extract_experience(self) -> Optional[str]:
        """Extract experience section"""
        experience_entries = []
        in_experience = False
        
        for i, line in enumerate(self.lines):
            line_lower = line.lower().strip()
            
            # Check if this is the start of experience section
            if 'professional experience' in line_lower or (line_lower.startswith('experience') and len(line_lower) < 20):
                in_experience = True
                continue
            
            # Check if we hit another section
            if in_experience:
                if any(keyword in line_lower for keyword in ['education', 'skills', 'projects', 'certification', 'awards']):
                    break
            
            # Collect job entries (lines with job titles and company names)
            if in_experience and line.strip():
                line_text = line.strip()
                # Look for lines that contain role and company info (e.g., "Title at Company (dates)")
                if any(role in line_lower for role in ['engineer', 'developer', 'analyst', 'manager', 'lead', 'architect', 'designer', 'scientist']):
                    if 'at ' in line_lower or re.search(r'\(\d{4}\s*-\s*(present|\d{4})\)', line_lower):
                        experience_entries.append(line_text)
        
        # Build experience string from first 2 entries
        if experience_entries:
            return ' | '.join(experience_entries[:2])
        
        return None
    
    def extract_projects(self) -> List[Dict[str, str]]:
        """Extract projects with name and description"""
        projects = []
        project_lines = []
        in_projects = False
        major_section_pattern = re.compile(r'^(education|skills|experience|professional experience|certification|awards|contact)\b', re.IGNORECASE)
        
        for i, line in enumerate(self.lines):
            line_lower = line.lower()
            
            # Check if this is the start of projects section
            if line_lower in ('projects', 'portfolio', 'personal projects') or line_lower.startswith('projects') or line_lower.startswith('personal projects'):
                in_projects = True
                continue
            
            # Check if we hit another section
            if in_projects and major_section_pattern.match(line_lower):
                in_projects = False
            
            # Collect project lines
            if in_projects:
                project_lines.append(line)
        
        # Parse projects from collected lines
        current_project = None
        for idx, line in enumerate(project_lines):
            next_line = project_lines[idx + 1] if idx + 1 < len(project_lines) else ''
            cleaned_line = line.strip()

            # Top-level bullet lines are project titles.
            if cleaned_line.startswith(('•', '*', '–', '—')):
                title = cleaned_line.lstrip('•*–—').strip()
                if title:
                    if current_project and current_project["title"]:
                        projects.append(current_project)
                    current_project = {"title": title, "description": ""}
                continue

            # Plain title lines can also start a project block when followed by bullet details.
            if cleaned_line and not cleaned_line.startswith('-') and next_line.startswith('-'):
                if current_project and current_project["title"]:
                    projects.append(current_project)
                current_project = {"title": cleaned_line, "description": ""}
                continue

            # Nested dash lines become project descriptions.
            if cleaned_line.startswith('-') and current_project:
                detail = cleaned_line[1:].strip()
                if detail:
                    if current_project["description"]:
                        current_project["description"] += " | " + detail
                    else:
                        current_project["description"] = detail
                continue

        if current_project:
            projects.append(current_project)
        
        return projects[:3]  # Limit to 3 projects
    
    def extract_all(self) -> Dict:
        """Extract all information"""
        return {
            "name": self.extract_name(),
            "email": self.extract_email(),
            "phone": self.extract_phone(),
            "linkedin": self.extract_linkedin(),
            "github": self.extract_github(),
            "technical_skills": self.extract_technical_skills(),
            "soft_skills": self.extract_soft_skills(),
            "summary": self.extract_summary(),
            "education": self.extract_education(),
            "experience": self.extract_experience(),
            "projects": self.extract_projects(),
        }
