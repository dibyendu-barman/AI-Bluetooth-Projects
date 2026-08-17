import sounddevice as sd
import soundfile as sf
import whisper
import os


# ==============================
# CONFIGURATION
# ==============================

MIC_DEVICE = 2
SAMPLE_RATE = 16000
CHANNELS = 1
DURATION = 5

AUDIO_FILE = "live_test.wav"
MODEL_NAME = "base"


# ==============================
# LOAD WHISPER
# ==============================

print("=" * 55)
print("   LIVE BLUETOOTH SPEECH-TO-TEXT TEST")
print("=" * 55)

print("\nLoading Whisper model...")

model = whisper.load_model(
    MODEL_NAME,
    device="cpu"
)

print("Whisper model loaded.")


# ==============================
# RECORD AUDIO
# ==============================

print("\n🎤 Get ready...")

input("Press ENTER to start recording...")

print("\n🎤 Recording for 5 seconds...")
print("Speak into your Airdopes Joy!")

audio = sd.rec(
    int(DURATION * SAMPLE_RATE),
    samplerate=SAMPLE_RATE,
    channels=CHANNELS,
    dtype="int16",
    device=MIC_DEVICE
)

sd.wait()

print("✅ Recording completed.")


# ==============================
# SAVE AUDIO
# ==============================

sf.write(
    AUDIO_FILE,
    audio,
    SAMPLE_RATE
)

print(f"Audio saved: {AUDIO_FILE}")


# ==============================
# SPEECH-TO-TEXT
# ==============================

print("\n🧠 Transcribing audio...")

result = model.transcribe(
    AUDIO_FILE,
    fp16=False
)

text = result["text"].strip()


# ==============================
# DISPLAY RESULT
# ==============================

print("\n" + "=" * 55)
print("   TRANSCRIPTION")
print("=" * 55)

print(text)

print("=" * 55)


# ==============================
# CLEANUP
# ==============================

if os.path.exists(AUDIO_FILE):
    os.remove(AUDIO_FILE)

print("\nTemporary audio file removed.")
print("✅ Live Speech-to-Text test completed.")