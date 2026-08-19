import librosa
import numpy as np
import matplotlib.pyplot as plt
import os


# ============================================================
# CONFIGURATION
# ============================================================

AUDIO_FILE = os.path.join("audio", "airdopes_test.wav")

OUTPUT_DIR = "reports"

OUTPUT_FILE = os.path.join(
    OUTPUT_DIR,
    "airdopes_spectral_features.png"
)


# ============================================================
# HEADER
# ============================================================

print("=" * 70)
print("AI MUSIC & AUDIO ANALYZER")
print("STEP 9 - SPECTRAL FEATURE ANALYSIS")
print("=" * 70)


# ============================================================
# CHECK AUDIO FILE
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
# SPECTRAL FEATURES
# ============================================================

spectral_centroid = librosa.feature.spectral_centroid(
    y=audio,
    sr=sample_rate
)[0]

spectral_bandwidth = librosa.feature.spectral_bandwidth(
    y=audio,
    sr=sample_rate
)[0]

spectral_rolloff = librosa.feature.spectral_rolloff(
    y=audio,
    sr=sample_rate,
    roll_percent=0.85
)[0]

spectral_flatness = librosa.feature.spectral_flatness(
    y=audio
)[0]

zero_crossing_rate = librosa.feature.zero_crossing_rate(
    audio
)[0]


# ============================================================
# CALCULATE AVERAGES
# ============================================================

centroid_mean = np.mean(spectral_centroid)

bandwidth_mean = np.mean(spectral_bandwidth)

rolloff_mean = np.mean(spectral_rolloff)

flatness_mean = np.mean(spectral_flatness)

zcr_mean = np.mean(zero_crossing_rate)


# ============================================================
# PRINT RESULTS
# ============================================================

print("\n" + "=" * 70)
print("SPECTRAL FEATURE RESULTS")
print("=" * 70)

print(
    f"Spectral Centroid  : {centroid_mean:.2f} Hz"
)

print(
    f"Spectral Bandwidth : {bandwidth_mean:.2f} Hz"
)

print(
    f"Spectral Rolloff   : {rolloff_mean:.2f} Hz"
)

print(
    f"Spectral Flatness  : {flatness_mean:.6f}"
)

print(
    f"Zero Crossing Rate : {zcr_mean:.6f}"
)


# ============================================================
# SIMPLE SOUND CHARACTERISTICS
# ============================================================

if centroid_mean < 1000:

    brightness = "Low / Dark"

elif centroid_mean < 3000:

    brightness = "Moderate"

else:

    brightness = "Bright"


if flatness_mean < 0.01:

    texture = "Tonal / Harmonic"

elif flatness_mean < 0.1:

    texture = "Mixed"

else:

    texture = "Noise-like"


print("\n" + "=" * 70)
print("SOUND CHARACTERISTICS")
print("=" * 70)

print(f"Brightness : {brightness}")
print(f"Texture    : {texture}")


# ============================================================
# CREATE FEATURE GRAPH
# ============================================================

feature_names = [
    "Centroid",
    "Bandwidth",
    "Rolloff"
]

feature_values = [
    centroid_mean,
    bandwidth_mean,
    rolloff_mean
]


plt.figure(figsize=(10, 5))

plt.bar(
    feature_names,
    feature_values
)

plt.title(
    "Airdopes Joy — Spectral Features"
)

plt.xlabel("Feature")

plt.ylabel("Frequency (Hz)")

plt.grid(
    axis="y",
    alpha=0.3
)

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
print("STEP 9 RESULT")
print("=" * 70)

print("✅ Spectral centroid calculated.")
print("✅ Spectral bandwidth calculated.")
print("✅ Spectral rolloff calculated.")
print("✅ Spectral flatness calculated.")
print("✅ Zero crossing rate calculated.")
print("✅ Sound characteristics estimated.")
print("✅ Feature graph generated.")

print("\nSaved graph:")
print(f"   {OUTPUT_FILE}")

print("\n🎵 STEP 9 COMPLETE")