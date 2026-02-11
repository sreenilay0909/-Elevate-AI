"""Test Gemini model access"""
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

# Configure Gemini
api_key = os.getenv('GEMINI_API_KEY')
print(f"API Key: {api_key[:20]}...")

genai.configure(api_key=api_key)

# Try gemini-flash-latest
print("\nTesting gemini-flash-latest model...")
try:
    model = genai.GenerativeModel('gemini-flash-latest')
    response = model.generate_content("Say hello in one sentence")
    print(f"✓ Success! Response: {response.text}")
except Exception as e:
    print(f"✗ Error: {e}")

# List available models
print("\nListing available models...")
try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"  - {m.name}")
except Exception as e:
    print(f"Error listing models: {e}")
