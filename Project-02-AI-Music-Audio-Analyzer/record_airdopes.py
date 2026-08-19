import sounddevice as sd
import soundfile as sf
import numpy as np
import os
import time

# ============================================================
# CONFIGURATION
# ============================================================

DEVICE_ID = 2
SAMPLE_RATE = 44100
CHANNELS = 1
DURATION = 5

OUTPUT_DIR = "audio"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "airdopes_test.wav")


# ============================================================
# HEADER
# ============================================================

print("=" * 70)
print("AI MUSIC & AUDIO ANALYZER")
print("STEP 3 - AIRDOPES AUDIO RECORDING")
print("=" * 70)


# ============================================================
# CREATE OUTPUT DIRECTORY
# ============================================================

os.makedirs(OUTPUT_DIR, exist_ok=True)


# ============================================================
# DEVICE INFORMATION
# ============================================================

device = sd.query_devices(DEVICE_ID)

print("\nSelected Audio Device")
print("-" * 70)
print(f"Device ID     : {DEVICE_ID}")
print(f"Device Name   : {device['name']}")
print(f"Input Channels: {device['max_input_channels']}")
print(f"Sample Rate   : {device['default_samplerate']} Hz")


# ============================================================
# COUNTDOWN
# ============================================================

print("\n🎧 Prepare your Airdopes microphone.")

for i in range(3, 0, -1):
    print(f"Starting in {i}...")
    time.sleep(1)


# ============================================================
# RECORD AUDIO
# ============================================================

print("\n🔴 RECORDING...")
print("Speak normally into your Airdopes.")
print(f"Recording duration: {DURATION} seconds\n")

try:

    audio = sd.rec(
        int(DURATION * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=CHANNELS,
        dtype="float32",
        device=DEVICE_ID
    )

    sd.wait()

    print("✅ Recording completed.")


    # ========================================================
    # BASIC AUDIO ANALYSIS
    # ========================================================

    audio_mono = audio.flatten()

    rms = np.sqrt(np.mean(audio_mono ** 2))
    peak = np.max(np.abs(audio_mono))

    print("\nAudio Information")
    print("-" * 70)
    print(f"Samples        : {len(audio_mono)}")
    print(f"Sample Rate    : {SAMPLE_RATE} Hz")
    print(f"Channels       : {CHANNELS}")
    print(f"Duration       : {len(audio_mono) / SAMPLE_RATE:.2f} sec")
    print(f"RMS Amplitude  : {rms:.6f}")
    print(f"Peak Amplitude : {peak:.6f}")


    # ========================================================
    # SAVE WAV FILE
    # ========================================================

    sf.write(
        OUTPUT_FILE,
        audio,
        SAMPLE_RATE
    )

    print("\n" + "=" * 70)
    print("RECORDING RESULT")
    print("=" * 70)

    print(f"✅ Audio saved successfully:")
    print(f"   {OUTPUT_FILE}")

    print("\n🎵 STEP 3 COMPLETE")


except Exception as error:

    print("\n" + "=" * 70)
    print("❌ RECORDING FAILED")
    print("=" * 70)

    print(f"Error: {error}")