def extract_skills(text):
    """
    Simple keyword-based skill extraction from resume text
    """
    skills_list = [
        "python", "java", "c++", "sql", "ml", "machine learning",
        "deep learning", "nlp", "fastapi", "streamlit", "tensorflow",
        "pandas", "numpy", "javascript", "html", "css", "react"
    ]

    text = text.lower()
    found_skills = []

    for skill in skills_list:
        if skill in text:
            # avoid duplicates
            if skill not in found_skills:
                found_skills.append(skill)

    return found_skills


def compare_progress(old_data, current_skills):
    """
    Compare previous memory with current skills
    """
    if not old_data:
        return "First session - no previous data found"

    old_skills = set(old_data.get("skills", []))
    new_skills = set(current_skills)

    gained = list(new_skills - old_skills)

    if gained:
        return f"New skills learned: {gained}"
    else:
        return "No improvement detected"


def get_missing_skills(current_skills):
    """
    Basic skill gap logic for internship readiness
    """
    required_skills = ["python", "sql", "ml"]

    missing = [skill for skill in required_skills if skill not in current_skills]

    return missing


def get_project_feedback(old_data, current_data):
    """
    Memory-based feedback for projects
    """
    old_projects = old_data.get("projects", []) if old_data else []
    current_projects = current_data.get("projects", [])

    if not old_projects and not current_projects:
        return "Last time you had no projects, still missing projects."
    elif not old_projects and current_projects:
        return "Great! You added projects since last session."
    elif len(current_projects) > len(old_projects):
        return "Nice progress! You added more projects."
    else:
        return "No new projects added."
