import time
import ollama


print("=" * 60)
print("          LOCAL AI INTEGRATION TEST")
print("=" * 60)

question = "What is Ohm's Law? Explain it in one simple sentence."

print("\nQuestion:")
print(question)

print("\n🤖 Sending question to local Gemma 4...")
print("⏳ Please wait...")

# Start timer
start_time = time.perf_counter()

response = ollama.chat(
    model="gemma4",
    messages=[
        {
            "role": "user",
            "content": question
        }
    ]
)

# Stop timer
end_time = time.perf_counter()

response_time = end_time - start_time

answer = response["message"]["content"].strip()


print("\n" + "=" * 60)
print("                 AI RESPONSE")
print("=" * 60)

print(answer)

print("=" * 60)

print(f"\n⏱️ AI Response Time: {response_time:.2f} seconds")

print("\n✅ Local AI integration test completed.")