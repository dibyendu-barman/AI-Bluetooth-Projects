import sounddevice as sd
import soundfile as sf

OUTPUT_DEVICE = 4
INPUT_FILE = "test_recording.wav"

print("=" * 50)
print("   BLUETOOTH EARBUD AUDIO PLAYBACK TEST")
print("=" * 50)

print("\nLoading recording...")

audio, sample_rate = sf.read(INPUT_FILE)

print(f"Sample rate: {sample_rate} Hz")
print("🔊 Playing through Airdopes Joy...")

sd.play(
    audio,
    sample_rate,
    device=OUTPUT_DEVICE
)

sd.wait()

print("Playback finished.")