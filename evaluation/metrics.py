import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"


class AtlasEvaluator:
    def __init__(self):
        self.api_key = os.getenv("GOOGLE_API_KEY")

    def evaluate(self, question, answer, context):
        """
        Evaluates the RAG response for Faithfulness and Relevance.
        Returns (faithfulness_score, relevance_score) as floats 0.0-1.0.
        """
        if not self.api_key:
            return 0, 0

        trimmed_context = context[:3000]
        prompt = f"""You are an AI Judge evaluating a RAG system.

1. Faithfulness: Is the answer derived purely from the context? (0.0 to 1.0)
2. Relevance: Does the answer directly address the user's question? (0.0 to 1.0)

Question: {question}
Answer: {answer}
Context: {trimmed_context}

Return ONLY valid JSON, no other text:
{{"faithfulness": <score>, "relevance": <score>}}"""

        try:
            resp = requests.post(
                f"{GEMINI_URL}?key={self.api_key}",
                json={
                    "contents": [{"parts": [{"text": prompt}]}],
                    "generationConfig": {
                        "temperature": 0,
                        "responseMimeType": "application/json",
                    },
                },
                timeout=60,
            )
            resp.raise_for_status()
            data = resp.json()
            text = data["candidates"][0]["content"]["parts"][0]["text"]
            scores = json.loads(text)
            return scores.get("faithfulness", 0), scores.get("relevance", 0)
        except Exception:
            return 0, 0