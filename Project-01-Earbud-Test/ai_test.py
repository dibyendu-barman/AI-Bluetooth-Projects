# $env:OPENAI_API_KEY="YOUR_API_KEY"
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
