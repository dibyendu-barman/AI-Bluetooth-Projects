import whisper


AUDIO_FILE = "test_recording.wav"
MODEL_NAME = "base"


print("=" * 50)
print("   SPEECH-TO-TEXT TEST")
print("=" * 50)

print("\nLoading Whisper model...")

model = whisper.load_model(MODEL_NAME, device="cpu")

print("Whisper model loaded.")

print("\nTranscribing audio...")

result = model.transcribe(
    AUDIO_FILE,
    fp16=False
)

text = result["text"].strip()

print("\n" + "=" * 50)
print("TRANSCRIPTION")
print("=" * 50)

print(text)

print("=" * 50)