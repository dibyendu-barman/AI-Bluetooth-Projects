import time
from google import genai

print("=" * 60)
print("       GEMINI CONCISE VOICE RESPONSE TEST")
print("=" * 60)

question = "Tell me about India."

client = genai.Client()

prompt = f"""
You are a Bluetooth earbud voice assistant.

Answer the user's question in simple, natural spoken English.

Rules:
- Maximum 3 sentences.
- No Markdown.
- No headings.
- No bullet points.
- No long explanations.
- Do not ask a follow-up question.
- Make the answer suitable for listening through earbuds.

User question:
{question}
"""

print(f"\nQuestion:\n{question}")
print("\n🤖 Gemini is thinking...")

start = time.perf_counter()

response = client.models.generate_content(
    model="gemini-3.1-flash-lite",
    contents=prompt
)

elapsed = time.perf_counter() - start

answer = response.text.strip()

print("\n" + "=" * 60)
print("             VOICE-FRIENDLY RESPONSE")
print("=" * 60)

print(answer)

print("=" * 60)
print(f"\n⏱️ Gemini response time: {elapsed:.2f} seconds")
print("\n✅ Concise response test completed.")