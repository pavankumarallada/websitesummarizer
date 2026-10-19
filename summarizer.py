import os
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
from scraper import fetch_website_contents

load_dotenv()          # <-- this reads your .env file
api_key = None

try:
    api_key = st.secrets["GROQ_API_KEY"]
except Exception:
    api_key = os.getenv("GROQ_API_KEY")

client = OpenAI(
    api_key=api_key,
    base_url="https://api.groq.com/openai/v1"
)

system_prompt = """You analyze the contents of a website and
give a short, friendly summary. Ignore navigation menus.
Respond in markdown."""

def summarize(url):
    website = fetch_website_contents(url) #function in scraper.py
    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {"role":"system", "content": system_prompt},
            {"role":"user",   "content": f"Summarize this website:\n\n{website}"},
        ],
    )
    return response.choices[0].message.content
