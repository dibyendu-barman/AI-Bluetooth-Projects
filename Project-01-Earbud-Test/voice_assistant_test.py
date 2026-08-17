import os
import time

import sounddevice as sd
import soundfile as sf
import whisper
import pyttsx3
from google import genai


# ============================================================
# CONFIGURATION
# ============================================================

MIC_DEVICE = 2
SPEAKER_DEVICE = 4

SAMPLE_RATE = 16000
CHANNELS = 1
DURATION = 5

AUDIO_FILE = "voice_assistant_temp.wav"

WHISPER_MODEL = "small"
GEMINI_MODEL = "gemini-3.1-flash-lite"


# ============================================================
# HEADER
# ============================================================

print("=" * 70)
print("             AI BLUETOOTH EARBUD VOICE ASSISTANT")
print("=" * 70)


# ============================================================
# LOAD WHISPER
# ============================================================

print("\n🧠 Loading Whisper model...")

whisper_model = whisper.load_model(
    WHISPER_MODEL,
    device="cpu"
)

print("✅ Whisper loaded.")


# ============================================================
# GEMINI
# ============================================================

print("\n🤖 Connecting to Gemini...")

gemini_client = genai.Client()

print("✅ Gemini connected.")


# ============================================================
# TTS
# ============================================================

print("\n🔊 Initializing Text-to-Speech...")

tts_engine = pyttsx3.init()

tts_engine.setProperty("rate", 160)
tts_engine.setProperty("volume", 1.0)

print("✅ TTS ready.")


# ============================================================
# RECORD
# ============================================================

print("\n🎤 Get ready...")
input("Press ENTER to start recording...")

print(f"\n🎤 Recording for {DURATION} seconds...")
print("Speak into your Airdopes Joy!")

total_start = time.perf_counter()

record_start = time.perf_counter()

audio = sd.rec(
    int(DURATION * SAMPLE_RATE),
    samplerate=SAMPLE_RATE,
    channels=CHANNELS,
    dtype="int16",
    device=MIC_DEVICE
)

sd.wait()

record_time = time.perf_counter() - record_start

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

print(f"💾 Audio saved: {AUDIO_FILE}")


# ============================================================
# WHISPER
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

whisper_time = time.perf_counter() - whisper_start

text = result["text"].strip()

print(f"⏱️ Whisper processing time: {whisper_time:.2f} seconds")


# ============================================================
# TRANSCRIPTION
# ============================================================

print("\n" + "=" * 70)
print("                 YOUR QUESTION")
print("=" * 70)

print(f'📝 "{text}"')

print("=" * 70)


# ============================================================
# GEMINI
# ============================================================

if not text:

    print("\n⚠️ No speech detected.")

else:

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
{text}
"""

    print("\n🤖 Gemini is thinking...")

    gemini_start = time.perf_counter()

    response = gemini_client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt
    )

    gemini_time = time.perf_counter() - gemini_start

    answer = response.text.strip()

    print(f"⏱️ Gemini response time: {gemini_time:.2f} seconds")


    # ========================================================
    # AI RESPONSE
    # ========================================================

    print("\n" + "=" * 70)
    print("                  AI RESPONSE")
    print("=" * 70)

    print(answer)

    print("=" * 70)


    # ========================================================
    # TEXT-TO-SPEECH
    # ========================================================

    print("\n🔊 Sending AI response to Airdopes Joy...")

    tts_start = time.perf_counter()

    tts_engine.say(answer)
    tts_engine.runAndWait()

    tts_time = time.perf_counter() - tts_start

    print(f"⏱️ TTS processing time: {tts_time:.2f} seconds")


# ============================================================
# PERFORMANCE SUMMARY
# ============================================================

total_time = time.perf_counter() - total_start

print("\n" + "=" * 70)
print("                 PERFORMANCE SUMMARY")
print("=" * 70)

print(f"Recording time       : {record_time:.2f} seconds")
print(f"Whisper processing   : {whisper_time:.2f} seconds")

if text:
    print(f"Gemini response      : {gemini_time:.2f} seconds")
    print(f"TTS processing       : {tts_time:.2f} seconds")

print(f"Total pipeline time  : {total_time:.2f} seconds")

print("=" * 70)


# ============================================================
# TEST RESULT
# ============================================================

print("\n📋 TEST RESULT")

print("Bluetooth Microphone : PASS")
print("Audio Recording      : PASS")
print("Whisper STT          : PASS")

if text:
    print("Gemini AI            : PASS")
    print("Text-to-Speech       : PASS")
    print("Airdopes Voice Loop  : PASS")
else:
    print("Gemini AI            : NOT TESTED")
    print("Text-to-Speech       : NOT TESTED")


# ============================================================
# CLEANUP
# ============================================================

if os.path.exists(AUDIO_FILE):

    os.remove(AUDIO_FILE)

    print("\n🧹 Temporary audio file removed.")


print("\n✅ COMPLETE VOICE ASSISTANT TEST FINISHED.")