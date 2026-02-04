import os
import google.generativeai as genai
from dotenv import load_dotenv

# Environment se key load karo
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    print("❌ Error: API Key nahi mili .env file mein!")
else:
    print(f"🔑 Key Found: {api_key[:5]}... (Checking Google Servers)")
    
    # Configure Google AI
    genai.configure(api_key=api_key)

    print("\n📋 Available Models for You:")
    print("-" * 30)
    try:
        # Google se pucho ki kaunse models available hain
        count = 0
        for m in genai.list_models():
            # Sirf wo models dikhao jo 'generateContent' (Chat) kar sakte hain
            if 'generateContent' in m.supported_generation_methods:
                print(f"✅ {m.name}")
                count += 1
        
        if count == 0:
            print("❌ Koi Chat Model nahi mila. Shayad API Key mein issue hai.")
    except Exception as e:
        print(f"❌ Error connecting to Google: {e}")