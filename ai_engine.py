
import streamlit as st
import time

from google import genai
from config import AI_MODELS
from prompts import SYSTEM_PROMPT


def get_client():

    try:
        api_key = st.secrets["GEMINI_API_KEY"]

        if not api_key:
            raise ValueError("API Key kosong")

        return genai.Client(api_key=api_key)

    except Exception as error:
        raise RuntimeError(
            "API Key Gemini tidak ditemukan. "
            "Periksa secrets.toml atau Streamlit Secrets."
        ) from error


def generate_answer(prompt, history=None):

    client = get_client()

    contents = []

    if history:
        contents.extend(history)

    contents.append({
        "role": "user",
        "parts": [{"text": prompt}]
    })

    last_error = None

    for model in AI_MODELS:

        for attempt in range(2):

            try:

                response = client.models.generate_content(
                    model=model,
                    contents=contents,
                    config={
                        "system_instruction": SYSTEM_PROMPT,
                        "temperature": 0.7
                    }
                )

                if response.text:
                    return response.text, model

                raise RuntimeError("AI tidak memberikan jawaban.")

            except Exception as error:

                last_error = error
                message = str(error).lower()

                temporary = any(code in message for code in [
                    "503", "429", "500", "502", "504",
                    "unavailable", "overloaded",
                    "resource_exhausted"
                ])

                if temporary and attempt == 0:
                    time.sleep(2)
                    continue

                break

    raise RuntimeError(
        f"AI gagal memberikan jawaban: {last_error}"
    )
