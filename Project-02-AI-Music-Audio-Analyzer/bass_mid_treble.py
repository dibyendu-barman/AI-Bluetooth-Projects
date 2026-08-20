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
    "airdopes_bass_mid_treble.png"
)


# Frequency bands
BASS_LOW = 20
BASS_HIGH = 250

MID_LOW = 250
MID_HIGH = 4000

TREBLE_LOW = 4000
TREBLE_HIGH = 20000


# ============================================================
# HEADER
# ============================================================

print("=" * 70)
print("AI MUSIC & AUDIO ANALYZER")
print("STEP 10 - BASS / MID / TREBLE ENERGY ANALYSIS")
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
# STFT
# ============================================================

N_FFT = 2048
HOP_LENGTH = 512

stft = librosa.stft(
    audio,
    n_fft=N_FFT,
    hop_length=HOP_LENGTH
)

magnitude = np.abs(stft)

frequencies = librosa.fft_frequencies(
    sr=sample_rate,
    n_fft=N_FFT
)


# ============================================================
# CREATE FREQUENCY MASKS
# ============================================================

bass_mask = (
    (frequencies >= BASS_LOW) &
    (frequencies < BASS_HIGH)
)

mid_mask = (
    (frequencies >= MID_LOW) &
    (frequencies < MID_HIGH)
)

treble_mask = (
    (frequencies >= TREBLE_LOW) &
    (frequencies <= TREBLE_HIGH)
)


# ============================================================
# CALCULATE ENERGY
# ============================================================

bass_energy = np.mean(
    magnitude[bass_mask] ** 2
)

mid_energy = np.mean(
    magnitude[mid_mask] ** 2
)

treble_energy = np.mean(
    magnitude[treble_mask] ** 2
)


# ============================================================
# TOTAL ENERGY
# ============================================================

total_energy = (
    bass_energy +
    mid_energy +
    treble_energy
)


# ============================================================
# ENERGY PERCENTAGE
# ============================================================

if total_energy > 0:

    bass_percent = (
        bass_energy / total_energy
    ) * 100

    mid_percent = (
        mid_energy / total_energy
    ) * 100

    treble_percent = (
        treble_energy / total_energy
    ) * 100

else:

    bass_percent = 0
    mid_percent = 0
    treble_percent = 0


# ============================================================
# PRINT RESULTS
# ============================================================

print("\n" + "=" * 70)
print("FREQUENCY BAND ENERGY")
print("=" * 70)

print(
    f"Bass   ({BASS_LOW}-{BASS_HIGH} Hz)"
    f" : {bass_energy:.6f}"
)

print(
    f"Mid    ({MID_LOW}-{MID_HIGH} Hz)"
    f" : {mid_energy:.6f}"
)

print(
    f"Treble ({TREBLE_LOW}-{TREBLE_HIGH} Hz)"
    f" : {treble_energy:.6f}"
)


print("\n" + "=" * 70)
print("ENERGY DISTRIBUTION")
print("=" * 70)

print(f"Bass   : {bass_percent:.2f}%")
print(f"Mid    : {mid_percent:.2f}%")
print(f"Treble : {treble_percent:.2f}%")

print(
    f"Total  : "
    f"{bass_percent + mid_percent + treble_percent:.2f}%"
)


# ============================================================
# DOMINANT BAND
# ============================================================

band_percentages = {
    "Bass": bass_percent,
    "Mid": mid_percent,
    "Treble": treble_percent
}

dominant_band = max(
    band_percentages,
    key=band_percentages.get
)


print("\n" + "=" * 70)
print("BAND CHARACTERISTIC")
print("=" * 70)

print(
    f"Dominant Frequency Band : "
    f"{dominant_band}"
)


# ============================================================
# CREATE BAR GRAPH
# ============================================================

bands = [
    "Bass",
    "Mid",
    "Treble"
]

percentages = [
    bass_percent,
    mid_percent,
    treble_percent
]


plt.figure(figsize=(9, 5))

plt.bar(
    bands,
    percentages
)

plt.title(
    "Airdopes Joy — Bass / Mid / Treble Energy"
)

plt.xlabel("Frequency Band")

plt.ylabel("Energy (%)")

plt.ylim(
    0,
    max(percentages) * 1.2
)

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
print("STEP 10 RESULT")
print("=" * 70)

print("✅ Bass energy calculated.")
print("✅ Mid energy calculated.")
print("✅ Treble energy calculated.")
print("✅ Energy percentages calculated.")
print("✅ Dominant frequency band identified.")
print("✅ Bass/Mid/Treble graph generated.")

print("\nSaved graph:")
print(f"   {OUTPUT_FILE}")

print("\n🎵 STEP 10 COMPLETE")