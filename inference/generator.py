import os
import requests
from dotenv import load_dotenv

load_dotenv()

GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"


class LLMGenerator:
    def __init__(self):
        self.api_key = os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            print("❌ Error: Google API Key missing")

        self.system_prompt = (
            "You are an expert AI Assistant named 'Atlas'.\n"
            "Use the following pieces of retrieved context to answer the question.\n"
            "If the answer is not in the context, just say that you don't know.\n"
            "Keep the answer concise and professional."
        )

    def generate(self, query, context):
        if not self.api_key:
            return "Error: LLM not initialized. Check API Key."

        prompt = f"""{self.system_prompt}

Context:
{context}

Question:
{query}

Answer:"""

        try:
            resp = requests.post(
                f"{GEMINI_URL}?key={self.api_key}",
                json={
                    "contents": [{"parts": [{"text": prompt}]}],
                    "generationConfig": {"temperature": 0.3},
                },
                timeout=60,
            )
            resp.raise_for_status()
            data = resp.json()
            return data["candidates"][0]["content"]["parts"][0]["text"]
        except Exception as e:
            return f"❌ Error generating response: {e}"
