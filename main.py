from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import openai
import os

# ---------- Data Model ----------
class InputText(BaseModel):
    text: str

# ---------- App Setup ----------
app = FastAPI()

# Allow frontend (Netlify) to call backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # you can restrict to your Netlify URL later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure OpenAI (expects OPENAI_API_KEY in environment variables)
openai.api_key = os.getenv("OPENAI_API_KEY")

# ---------- Routes ----------
@app.get("/")
def root():
    return {"message": "OneWay AI backend is live 🚀"}

@app.post("/repurpose")
def repurpose(input_data: InputText):
    text = input_data.text.strip()

    # If API key missing, return stubbed responses
    if not openai.api_key:
        return {
            "x_thread": f"🧵 OneWay AI Repurposed Thread\n\n1/ {text[:120]}...\n2/ Key takeaway 1 here\n3/ Key takeaway 2 here\n4/ CTA: Follow for more insights 🚀",
            "linkedin_post": f"🚀 {text[:180]}...\n\n👉 Practical insights, tailored for professionals.\n#Leadership #AI #Productivity",
            "newsletter": f"✉️ OneWay AI Newsletter Draft\n\n{ text[:250] }\n\n— End of preview —\n(P.S. This was repurposed automatically 😉)"
        }

    # Call OpenAI (Chat Completions API)
    prompt = f"""Repurpose this text into 3 formats:

1. X thread (short, engaging, numbered).
2. LinkedIn post (professional tone, hashtags).
3. Newsletter draft (conversational, email-style).

Text: {text}
"""

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=800,
        temperature=0.7
    )

    output = response.choices[0].message["content"]

    # Naive split (assumes model follows instructions cleanly)
    parts = output.split("\n\n")

    return {
        "x_thread": parts[0] if len(parts) > 0 else "",
        "linkedin_post": parts[1] if len(parts) > 1 else "",
        "newsletter": parts[2] if len(parts) > 2 else ""
    }
