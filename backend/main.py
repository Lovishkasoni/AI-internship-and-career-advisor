from fastapi import FastAPI
from pydantic import BaseModel
from llm import generate_response
from memory import store_memory, get_memory
from utils import extract_skills, compare_progress, get_missing_skills, extract_projects, get_project_feedback

app = FastAPI()

# -------- Input Model --------
class UserInput(BaseModel):
    user_id: str
    resume_text: str

# -------- Main API --------
@app.post("/analyze")
def analyze(data: UserInput):
    # 1. Extract skills AND projects
    current_skills = extract_skills(data.resume_text)
    current_projects = extract_projects(data.resume_text)  

    # 2. Build current data correctly
    current_data = {
        "skills": current_skills,
        "projects": current_projects,   
        "goal": "internship"
    }

    # 3. Get old memory
    old_data = get_memory(data.user_id)

    # 4. Logic from utils.py
    improvement = compare_progress(old_data, current_skills)
    missing_skills = get_missing_skills(current_skills)
    project_feedback = get_project_feedback(old_data, current_data)

    # 5. Save updated memory
    store_memory(data.user_id, current_data)

    # 6. LLM Prompt
    prompt = f"""
Previous data: {old_data}
Current data: {current_data}

Improvement: {improvement}
Missing skills: {missing_skills}
Project feedback: {project_feedback}

Give personalized career advice for internship.
If no improvement, be strict.
"""

    advice = generate_response(prompt)

    return {
        "skills": current_skills,
        "projects": current_projects,  
        "missing_skills": missing_skills,
        "improvement": improvement,
        "project_feedback": project_feedback,
        "advice": advice
    }
# -------- Test Route --------
@app.get("/")
def home():
    return {"message": "Backend running 🚀"}