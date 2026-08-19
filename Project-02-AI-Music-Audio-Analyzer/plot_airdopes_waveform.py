import librosa
import numpy as np
import matplotlib.pyplot as plt
import os


# ============================================================
# CONFIGURATION
# ============================================================

AUDIO_FILE = os.path.join("audio", "airdopes_test.wav")
OUTPUT_DIR = "reports"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "airdopes_waveform.png")


# ============================================================
# HEADER
# ============================================================

print("=" * 70)
print("AI MUSIC & AUDIO ANALYZER")
print("STEP 5 - WAVEFORM VISUALIZATION")
print("=" * 70)


# ============================================================
# CHECK AUDIO FILE
# ============================================================

if not os.path.exists(AUDIO_FILE):

    print("\n❌ Audio file not found!")
    print(f"Expected: {AUDIO_FILE}")
    exit()


# ============================================================
# CREATE REPORT DIRECTORY
# ============================================================

os.makedirs(OUTPUT_DIR, exist_ok=True)


# ============================================================
# LOAD AUDIO
# ============================================================

try:

    audio, sample_rate = librosa.load(
        AUDIO_FILE,
        sr=None,
        mono=True
    )

    print("\n✅ Audio loaded successfully.")

except Exception as error:

    print("\n❌ Failed to load audio.")
    print(f"Error: {error}")
    exit()


# ============================================================
# AUDIO INFORMATION
# ============================================================

samples = len(audio)
duration = samples / sample_rate

print("\nAudio Information")
print("-" * 70)
print(f"Sample Rate : {sample_rate} Hz")
print(f"Samples     : {samples}")
print(f"Duration    : {duration:.2f} seconds")


# ============================================================
# CREATE TIME AXIS
# ============================================================

time = np.arange(samples) / sample_rate


# ============================================================
# CALCULATE SIGNAL LEVEL
# ============================================================

rms = np.sqrt(np.mean(audio ** 2))
peak = np.max(np.abs(audio))

if rms > 0:
    rms_dbfs = 20 * np.log10(rms)
else:
    rms_dbfs = float("-inf")

if peak > 0:
    peak_dbfs = 20 * np.log10(peak)
else:
    peak_dbfs = float("-inf")


# ============================================================
# CREATE WAVEFORM
# ============================================================

plt.figure(figsize=(12, 5))

plt.plot(time, audio)

plt.title("Airdopes Joy Microphone — Audio Waveform")
plt.xlabel("Time (seconds)")
plt.ylabel("Amplitude")

plt.xlim(0, duration)
plt.ylim(-1, 1)

plt.grid(True, alpha=0.3)

plt.tight_layout()


# ============================================================
# SAVE IMAGE
# ============================================================

plt.savefig(
    OUTPUT_FILE,
    dpi=150,
    bbox_inches="tight"
)

plt.show()


# ============================================================
# RESULT
# ============================================================

print("\n" + "=" * 70)
print("WAVEFORM ANALYSIS RESULT")
print("=" * 70)

print(f"RMS Level  : {rms_dbfs:.2f} dBFS")
print(f"Peak Level : {peak_dbfs:.2f} dBFS")

print("\n✅ Waveform generated successfully.")
print(f"✅ Saved to: {OUTPUT_FILE}")

print("\n🎵 STEP 5 COMPLETE")