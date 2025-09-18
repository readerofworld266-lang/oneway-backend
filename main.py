from fastapi import FastAPI
from pydantic import BaseModel
import os
from openai import OpenAI

app = FastAPI()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class InputText(BaseModel):
    text: str

@app.post("/repurpose")
async def repurpose_content(input: InputText):
    # Prompt for OpenAI
    prompt = f"""
    Take the following text and repurpose it into 3 formats:
    1. A short, engaging Twitter/X post (280 characters max).
    2. A professional LinkedIn post (2–3 sentences).
    3. A newsletter introduction (1–2 short paragraphs).

    Text: {input.text}
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=400
    )

    # Extract output
    output = response.choices[0].message.content

    # Basic parsing: split into 3 sections
    parts = output.split("\n")
    twitter, linkedin, newsletter = "", "", ""
    section = None
    for line in parts:
        if line.strip().startswith("1"):
            section = "twitter"
            continue
        elif line.strip().startswith("2"):
            section = "linkedin"
            continue
        elif line.strip().startswith("3"):
            section = "newsletter"
            continue

        if section == "twitter":
            twitter += line.strip() + " "
        elif section == "linkedin":
            linkedin += line.strip() + " "
        elif section == "newsletter":
            newsletter += line.strip() + " "

    return {
        "twitter": twitter.strip(),
        "linkedin": linkedin.strip(),
        "newsletter": newsletter.strip()
    }
