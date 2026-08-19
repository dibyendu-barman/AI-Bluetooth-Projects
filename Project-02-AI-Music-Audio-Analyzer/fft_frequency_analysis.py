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
    "airdopes_frequency_spectrum.png"
)


# ============================================================
# HEADER
# ============================================================

print("=" * 70)
print("AI MUSIC & AUDIO ANALYZER")
print("STEP 7 - FFT / FREQUENCY SPECTRUM ANALYSIS")
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
# APPLY WINDOW FUNCTION
# ============================================================

window = np.hanning(len(audio))

windowed_audio = audio * window


# ============================================================
# FFT
# ============================================================

fft_result = np.fft.rfft(windowed_audio)

magnitude = np.abs(fft_result)


# ============================================================
# FREQUENCY AXIS
# ============================================================

frequencies = np.fft.rfftfreq(
    len(audio),
    d=1 / sample_rate
)


# ============================================================
# NORMALIZE MAGNITUDE
# ============================================================

magnitude = magnitude / len(audio)

magnitude_db = 20 * np.log10(
    magnitude + 1e-12
)


# ============================================================
# FIND DOMINANT FREQUENCY
# ============================================================

dominant_index = np.argmax(magnitude)

dominant_frequency = frequencies[dominant_index]

dominant_magnitude = magnitude[dominant_index]


# ============================================================
# PRINT FFT RESULTS
# ============================================================

print("\n" + "=" * 70)
print("FFT ANALYSIS")
print("=" * 70)

print(f"FFT Samples          : {len(fft_result)}")
print(f"Frequency Resolution : {sample_rate / samples:.4f} Hz")
print(f"Maximum Frequency    : {sample_rate / 2:.0f} Hz")

print(f"\nDominant Frequency   : {dominant_frequency:.2f} Hz")
print(f"Dominant Magnitude   : {dominant_magnitude:.6f}")


# ============================================================
# LIMIT DISPLAY RANGE
# ============================================================

MAX_DISPLAY_FREQUENCY = 10000

frequency_mask = frequencies <= MAX_DISPLAY_FREQUENCY


display_frequencies = frequencies[frequency_mask]

display_magnitude = magnitude_db[frequency_mask]


# ============================================================
# CREATE FREQUENCY SPECTRUM
# ============================================================

plt.figure(figsize=(12, 5))

plt.plot(
    display_frequencies,
    display_magnitude
)

plt.title(
    "Airdopes Joy Microphone — Frequency Spectrum"
)

plt.xlabel("Frequency (Hz)")

plt.ylabel("Magnitude (dB)")

plt.xlim(0, MAX_DISPLAY_FREQUENCY)

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
print("STEP 7 RESULT")
print("=" * 70)

print("✅ FFT calculation completed.")
print("✅ Frequency axis generated.")
print("✅ Magnitude spectrum calculated.")
print("✅ Dominant frequency identified.")
print("✅ Frequency spectrum graph generated.")

print(f"\n✅ Saved graph:")
print(f"   {OUTPUT_FILE}")

print("\n🎵 STEP 7 COMPLETE")