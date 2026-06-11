import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    print("❌ Error: API Key not found!")
else:
    genai.configure(api_key=api_key)
    print("📋 Checking available Embedding models for your API Key...")
    found = False
    try:
        for m in genai.list_models():
            if 'embedContent' in m.supported_generation_methods:
                print(f"✅ Found: {m.name}")
                found = True
        if not found:
            print("❌ No embedding models found. Check your API Key permissions.")
    except Exception as e:
        print(f"❌ Error listing models: {e}")
