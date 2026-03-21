from fastapi import FastAPI
from pydantic import BaseModel
from llm import generate_response
from memory import store_memory, get_memory

app = FastAPI()

# -------- Input Schema --------
class UserInput(BaseModel):
    user_id: str
    resume_text: str

# -------- Skill Extraction --------
def extract_skills(text):
    skills_list = ["python", "ml", "sql", "nlp"]
    text = text.lower()
    return [s for s in skills_list if s in text]

# -------- Main API --------
@app.post("/analyze")
def analyze(data: UserInput):

    current_skills = extract_skills(data.resume_text)

    current_data = {
        "skills": current_skills,
        "projects": [],
        "goal": "internship"
    }

    old_data = get_memory(data.user_id)

    improvement = ""

    if old_data:
        old_skills = set(old_data.get("skills", []))
        new_skills = set(current_skills)

        gained = list(new_skills - old_skills)

        if gained:
            improvement = f"New skills learned: {gained}"
        else:
            improvement = "No improvement detected"

    store_memory(data.user_id, current_data)

    # ADD THIS BLOCK RIGHT HERE
    prompt = f"""
    Previous data: {old_data}
    Current data: {current_data}

    Improvement: {improvement}

    Give personalized career advice for internship.
    If no improvement, be strict.
    """

    advice = generate_response(prompt)

    #  MODIFY RETURN
    return {
        "skills": current_skills,
        "improvement": improvement,
        "advice": advice
    }
# -------- Test Route --------
@app.get("/")
def home():
    return {"message": "Backend running 🚀"}