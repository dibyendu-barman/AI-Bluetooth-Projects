# $env:GEMINI_API_KEY="AQ.Ab8RN6JBTraLq2vUR79GFyA5AyeSO58ef3JnGzLdoWAMVXP8PA"
# if ($env:GEMINI_API_KEY) { "Gemini API key configured" } else { "Gemini API key missing" }

import time
from google import genai


print("=" * 60)
print("           GEMINI API INTEGRATION TEST")
print("=" * 60)

question = "What is Ohm's Law? Explain it in one simple sentence."

print("\nQuestion:")
print(question)

print("\n🤖 Sending question to Gemini...")
print("⏳ Please wait...")

client = genai.Client()

start_time = time.perf_counter()

response = client.models.generate_content(
    model="gemini-3.1-flash-lite",
    contents=question
)

end_time = time.perf_counter()

response_time = end_time - start_time

print("\n" + "=" * 60)
print("                 AI RESPONSE")
print("=" * 60)

print(response.text)

print("=" * 60)

print(f"\n⏱️ Gemini Response Time: {response_time:.2f} seconds")

print("\n✅ Gemini API integration test completed.")