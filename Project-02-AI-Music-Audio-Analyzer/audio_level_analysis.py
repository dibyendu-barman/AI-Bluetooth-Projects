import librosa
import numpy as np
import matplotlib.pyplot as plt
import os


# ============================================================
# CONFIGURATION
# ============================================================

AUDIO_FILE = os.path.join("audio", "airdopes_test.wav")
OUTPUT_DIR = "reports"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "airdopes_audio_level.png")


# ============================================================
# HEADER
# ============================================================

print("=" * 70)
print("AI MUSIC & AUDIO ANALYZER")
print("STEP 6 - AUDIO LEVEL ANALYSIS")
print("=" * 70)


# ============================================================
# CHECK FILE
# ============================================================

if not os.path.exists(AUDIO_FILE):

    print("\n❌ Audio file not found!")
    print(f"Expected: {AUDIO_FILE}")
    exit()


# ============================================================
# CREATE OUTPUT DIRECTORY
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
# BASIC INFORMATION
# ============================================================

samples = len(audio)
duration = samples / sample_rate

print("\nAudio Information")
print("-" * 70)

print(f"Sample Rate : {sample_rate} Hz")
print(f"Samples     : {samples}")
print(f"Duration    : {duration:.2f} seconds")


# ============================================================
# BASIC LEVEL VALUES
# ============================================================

rms = np.sqrt(np.mean(audio ** 2))

peak = np.max(np.abs(audio))

minimum = np.min(audio)

maximum = np.max(audio)

mean_absolute = np.mean(np.abs(audio))


# ============================================================
# dBFS
# ============================================================

if rms > 0:
    rms_dbfs = 20 * np.log10(rms)
else:
    rms_dbfs = float("-inf")


if peak > 0:
    peak_dbfs = 20 * np.log10(peak)
else:
    peak_dbfs = float("-inf")


# ============================================================
# CREST FACTOR
# ============================================================

if rms > 0:
    crest_factor = peak / rms
else:
    crest_factor = 0


# ============================================================
# LEVEL CLASSIFICATION
# ============================================================

if peak_dbfs >= -3:

    level_status = "Very High"

elif peak_dbfs >= -6:

    level_status = "High"

elif peak_dbfs >= -12:

    level_status = "Healthy"

elif peak_dbfs >= -24:

    level_status = "Moderate"

else:

    level_status = "Low"


# ============================================================
# PRINT RESULTS
# ============================================================

print("\n" + "=" * 70)
print("AUDIO LEVEL RESULTS")
print("=" * 70)

print(f"Minimum Amplitude       : {minimum:.6f}")
print(f"Maximum Amplitude       : {maximum:.6f}")
print(f"Mean Absolute Amplitude : {mean_absolute:.6f}")
print(f"RMS Amplitude           : {rms:.6f}")
print(f"Peak Amplitude          : {peak:.6f}")

print(f"\nRMS Level               : {rms_dbfs:.2f} dBFS")
print(f"Peak Level              : {peak_dbfs:.2f} dBFS")

print(f"\nCrest Factor            : {crest_factor:.3f}")

print(f"Level Classification    : {level_status}")


# ============================================================
# RMS LEVEL OVER TIME
# ============================================================

window_size = int(sample_rate * 0.1)

rms_values = []
time_values = []


for start in range(0, len(audio), window_size):

    end = min(start + window_size, len(audio))

    segment = audio[start:end]

    if len(segment) == 0:
        continue

    segment_rms = np.sqrt(np.mean(segment ** 2))

    if segment_rms > 0:

        segment_dbfs = 20 * np.log10(segment_rms)

    else:

        segment_dbfs = -100

    rms_values.append(segment_dbfs)

    time_values.append(start / sample_rate)


# ============================================================
# CREATE GRAPH
# ============================================================

plt.figure(figsize=(12, 5))

plt.plot(time_values, rms_values)

plt.title("Airdopes Joy Microphone — RMS Audio Level")

plt.xlabel("Time (seconds)")

plt.ylabel("RMS Level (dBFS)")

plt.xlim(0, duration)

plt.grid(True, alpha=0.3)

plt.tight_layout()


# ============================================================
# SAVE GRAPH
# ============================================================

plt.savefig(
    OUTPUT_FILE,
    dpi=150,
    bbox_inches="tight"
)

plt.show()


# ============================================================
# FINAL RESULT
# ============================================================

print("\n" + "=" * 70)
print("STEP 6 RESULT")
print("=" * 70)

print("✅ Audio level analysis completed.")
print("✅ RMS level calculated.")
print("✅ Peak level calculated.")
print("✅ dBFS levels calculated.")
print("✅ Crest factor calculated.")
print("✅ RMS level graph generated.")

print(f"\n✅ Saved graph:")
print(f"   {OUTPUT_FILE}")

print("\n🎵 STEP 6 COMPLETE")