
import os
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv

from scraper import fetch_website_contents

# Load local .env for local development
load_dotenv()

SYSTEM_PROMPT = """
You analyze the contents of a website and give a short, friendly summary.
Ignore navigation menus.
Summarize only the content provided.
Do not invent information that is not present in the content.
Respond in markdown.
"""


def get_api_key():
    """Get the API key from Streamlit Secrets or local .env."""

    try:
        api_key = st.secrets.get("GROQ_API_KEY")
    except Exception:
        api_key = None

    if not api_key:
        api_key = os.getenv("GROQ_API_KEY")

    return api_key


def summarize(url):
    api_key = get_api_key()

    if not api_key:
        raise ValueError(
            "GROQ_API_KEY not found. Add it to Streamlit Secrets "
            "or your local .env file."
        )

    # Fetch the webpage first.
    # If fetching fails, the error propagates to app.py.
    website_content = fetch_website_contents(url)

    client = OpenAI(
        api_key=api_key,
        base_url="https://api.groq.com/openai/v1"
    )

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": (
                    "Summarize this website in a short, friendly format. "
                    "Use headings or bullet points where helpful.\n\n"
                    f"{website_content}"
                )
            }
        ],
        temperature=0.2,
        max_tokens=800
    )

    summary = response.choices[0].message.content

    if not summary:
        raise RuntimeError("The AI model returned an empty summary.")

    return summary
