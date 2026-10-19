import os
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv

from scraper import fetch_website_contents

# Load local .env (for local development)
load_dotenv()

SYSTEM_PROMPT = """
You analyze the contents of a website and give a short, friendly summary.
Ignore navigation menus.
Respond in markdown.
"""


def get_api_key():
    """
    Get API key from Streamlit Secrets first,
    then from local .env file.
    """

    try:
        return st.secrets["GROQ_API_KEY"]
    except Exception:
        return os.getenv("GROQ_API_KEY")


def summarize(url):

    api_key = get_api_key()

    if not api_key:
        raise ValueError(
            "GROQ_API_KEY not found. "
            "Add it to Streamlit Secrets or your .env file."
        )

    client = OpenAI(
        api_key=api_key,
        base_url="https://api.groq.com/openai/v1"
    )

    website_content = fetch_website_contents(url)

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": f"Summarize this website:\n\n{website_content}"
            }
        ]
    )

    return response.choices[0].message.content