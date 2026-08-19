import sounddevice as sd
import numpy as np
import time

DEVICE_ID = 2
SAMPLE_RATE = 44100
CHANNELS = 1
DURATION = 5

print("=" * 70)
print("AI MUSIC & AUDIO ANALYZER")
print("AIRDOPES MICROPHONE TEST")
print("=" * 70)

device = sd.query_devices(DEVICE_ID)

print("\nSelected Device:")
print(f"Name        : {device['name']}")
print(f"Input       : {device['max_input_channels']} channel(s)")
print(f"Sample Rate : {device['default_samplerate']} Hz")

print("\n🎤 Prepare your Airdopes microphone.")

for i in range(3, 0, -1):
    print(f"Starting in {i}...")
    time.sleep(1)

print("\n🔴 RECORDING")
print("Speak normally into your Airdopes.")
print("Recording for 5 seconds...\n")

try:
    audio = sd.rec(
        int(DURATION * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=CHANNELS,
        dtype="float32",
        device=DEVICE_ID
    )

    sd.wait()

    audio = audio.flatten()

    rms = np.sqrt(np.mean(audio ** 2))
    peak = np.max(np.abs(audio))

    print("\n" + "=" * 70)
    print("MICROPHONE TEST RESULT")
    print("=" * 70)

    print(f"Samples       : {len(audio)}")
    print(f"RMS Amplitude : {rms:.6f}")
    print(f"Peak Amplitude: {peak:.6f}")

    if peak > 0.01:
        print("\n✅ Audio signal detected!")
        print("✅ Airdopes microphone is working with Python.")
    else:
        print("\n⚠️ Very low/no audio signal detected.")

except Exception as e:
    print("\n❌ Microphone test failed.")
    print("Error:", e)