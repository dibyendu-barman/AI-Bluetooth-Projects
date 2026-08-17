# $env:GEMINI_API_KEY="YOUR_GEMINI_API_KEY"
# if ($env:GEMINI_API_KEY) { "Gemini API key configured" } else { "Gemini API key missing" }

import time

import sounddevice as sd
import soundfile as sf
import whisper
from google import genai


# ============================================================
# CONFIGURATION
# ============================================================

MIC_DEVICE = 2
SAMPLE_RATE = 16000
CHANNELS = 1
DURATION = 5

AUDIO_FILE = "whisper_gemini_temp.wav"

WHISPER_MODEL = "small"
GEMINI_MODEL = "gemini-3.1-flash-lite"


# ============================================================
# HEADER
# ============================================================

print("=" * 65)
print("       WHISPER → GEMINI AI INTEGRATION TEST")
print("=" * 65)


# ============================================================
# LOAD WHISPER
# ============================================================

print("\n🧠 Loading Whisper model...")

whisper_model = whisper.load_model(
    WHISPER_MODEL,
    device="cpu"
)

print("✅ Whisper model loaded.")


# ============================================================
# GEMINI CLIENT
# ============================================================

print("\n🤖 Connecting to Gemini...")

gemini_client = genai.Client()

print("✅ Gemini client ready.")


# ============================================================
# RECORD AUDIO
# ============================================================

print("\n🎤 Get ready...")
input("Press ENTER to start recording...")

print(f"\n🎤 Recording for {DURATION} seconds...")
print("Speak into your Airdopes Joy!")

record_start = time.perf_counter()

audio = sd.rec(
    int(DURATION * SAMPLE_RATE),
    samplerate=SAMPLE_RATE,
    channels=CHANNELS,
    dtype="int16",
    device=MIC_DEVICE
)

sd.wait()

record_end = time.perf_counter()

record_time = record_end - record_start

print("✅ Recording completed.")
print(f"⏱️ Recording time: {record_time:.2f} seconds")


# ============================================================
# SAVE AUDIO
# ============================================================

sf.write(
    AUDIO_FILE,
    audio,
    SAMPLE_RATE
)

print(f"💾 Temporary audio saved: {AUDIO_FILE}")


# ============================================================
# WHISPER SPEECH-TO-TEXT
# ============================================================

print("\n🧠 Whisper is transcribing...")

whisper_start = time.perf_counter()

result = whisper_model.transcribe(
    AUDIO_FILE,
    language="en",
    fp16=False,
    temperature=0,
    condition_on_previous_text=False
)

whisper_end = time.perf_counter()

whisper_time = whisper_end - whisper_start

text = result["text"].strip()

print(f"⏱️ Whisper processing time: {whisper_time:.2f} seconds")

print("\n" + "=" * 65)
print("              WHISPER TRANSCRIPTION")
print("=" * 65)

print(f'📝 "{text}"')

print("=" * 65)

input("\nPress ENTER to send this transcription to Gemini...")

# ============================================================
# DISPLAY TRANSCRIPTION
# ============================================================

print("\n" + "=" * 65)
print("                 TRANSCRIPTION")
print("=" * 65)

print(text)

print("=" * 65)


# ============================================================
# GEMINI AI
# ============================================================

if not text:
    print("\n⚠️ No speech detected.")
else:

    print("\n🤖 Sending transcription to Gemini...")
    print("⏳ Gemini is processing...")

    gemini_start = time.perf_counter()

    response = gemini_client.models.generate_content(
        model=GEMINI_MODEL,
        contents=text
    )

    gemini_end = time.perf_counter()

    gemini_time = gemini_end - gemini_start

    answer = response.text.strip()

    print(f"⏱️ Gemini response time: {gemini_time:.2f} seconds")

    print("\n" + "=" * 65)
    print("                    AI RESPONSE")
    print("=" * 65)

    print(answer)

    print("=" * 65)


# ============================================================
# TOTAL PROCESSING TIME
# ============================================================

total_end = time.perf_counter()

total_time = total_end - record_start

print("\n📊 PERFORMANCE SUMMARY")
print("=" * 65)

print(f"Recording time       : {record_time:.2f} seconds")
print(f"Whisper processing   : {whisper_time:.2f} seconds")

if text:
    print(f"Gemini response      : {gemini_time:.2f} seconds")

print(f"Total pipeline time  : {total_time:.2f} seconds")

print("=" * 65)


# ============================================================
# CLEANUP
# ============================================================

try:
    import os

    if os.path.exists(AUDIO_FILE):
        os.remove(AUDIO_FILE)
        print("\n🧹 Temporary audio file removed.")

except OSError as error:
    print(f"\n⚠️ Could not remove temporary file: {error}")


print("\n✅ Whisper → Gemini integration test completed.")
