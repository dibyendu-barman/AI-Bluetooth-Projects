# $env:OPENAI_API_KEY="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"
# if ($env:OPENAI_API_KEY) { "API key is configured" } else { "API key is missing" }
from openai import OpenAI


print("=" * 55)
print("        AI INTEGRATION TEST")
print("=" * 55)

client = OpenAI()

question = "What is Ohm's Law? Explain it in one simple sentence."

print("\nQuestion:")
print(question)

print("\n🤖 Asking AI...")

response = client.responses.create(
    model="gpt-5.5",
    input=question
)

answer = response.output_text

print("\n" + "=" * 55)
print("        AI RESPONSE")
print("=" * 55)

print(answer)

print("=" * 55)
print("\n✅ AI integration test completed.")