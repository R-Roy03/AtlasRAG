import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    print("❌ Error: API Key not found!")
else:
    genai.configure(api_key=api_key)
    print("📋 Checking available CHAT models...")
    try:
        for m in genai.list_models():
            # find models for 'generateContent' method (chat models)
            if 'generateContent' in m.supported_generation_methods:
                print(f"✅ Found: {m.name}")
    except Exception as e:
        print(f"❌ Error listing models: {e}")