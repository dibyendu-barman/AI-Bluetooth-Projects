import time
import pyttsx3

print("=" * 60)
print("             TEXT-TO-SPEECH TEST")
print("=" * 60)

text = (
    "India is a vast and vibrant country in South Asia "
    "known for its incredible cultural diversity and rich history."
)

print("\nText to speak:")
print(text)

engine = pyttsx3.init()

# Speech settings
engine.setProperty("rate", 160)
engine.setProperty("volume", 1.0)

print("\n🔊 Speaking through the default Windows audio output...")

start = time.perf_counter()

engine.say(text)
engine.runAndWait()

elapsed = time.perf_counter() - start

print(f"\n⏱️ TTS processing time: {elapsed:.2f} seconds")
print("\n✅ Text-to-Speech test completed.")