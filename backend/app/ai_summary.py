import anthropic
import os
import json
import re
from dotenv import load_dotenv

load_dotenv()
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def generateContent(goals_list, reflections_list, week_start, week_end):
    prompt = f"""
        You are a helpful personal growth assistant.
        The user has the following **big-picture goals**:
        {goals_list}

        Here are the user's **daily reflections for the week of {week_start} to {week_end}**:
        {reflections_list}

        Instructions:

        1. Write a **short narrative summary** of the week (3-5 sentences) that reflects what the user accomplished, any patterns in energy or mood, and progress toward goals.
        2. Identify **which goals were actively worked toward** this week. List them as bullet points.
        3. Suggest **3–5 specific, realistic next steps** for the upcoming week that move the user toward their big-picture goals.
        4. Output your answer in the following **JSON format** ONLY:

        {{
        "summary_text": "Your weekly summary here.",
        "goals_worked_on": ["Goal 1", "Goal 2", ...],
        "next_steps": ["Next step 1", "Next step 2", ...],
        "week_start": "{week_start}",
        "week_end": "{week_end}"
        }}

        Do NOT include anything outside the JSON. Do NOT wrap it in markdown code blocks or backticks.
        Output raw JSON only, starting with {{ and ending with }}.
        Keep the tone encouraging, practical, and concise.
        """
    print("Generating content...")
    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    raw = message.content[0].text
    cleaned = re.sub(r"^```(?:json)?\s*|\s*```$", "", raw.strip())
    return json.loads(cleaned)
