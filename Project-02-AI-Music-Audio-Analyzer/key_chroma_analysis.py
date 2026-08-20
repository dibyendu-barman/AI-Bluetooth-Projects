import librosa
import numpy as np
import matplotlib.pyplot as plt
import os


# ============================================================
# CONFIGURATION
# ============================================================

MUSIC_FILE = os.path.join(
    "music",
    "test_music.mp3"
)

REPORT_DIR = "reports"

OUTPUT_FILE = os.path.join(
    REPORT_DIR,
    "music_key_chroma.png"
)


# ============================================================
# MUSICAL NOTES
# ============================================================

NOTE_NAMES = [
    "C",
    "C#",
    "D",
    "D#",
    "E",
    "F",
    "F#",
    "G",
    "G#",
    "A",
    "A#",
    "B"
]


# ============================================================
# MAJOR KEY PROFILES
# Krumhansl-Schmuckler
# ============================================================

MAJOR_PROFILE = np.array([
    6.35,
    2.23,
    3.48,
    2.33,
    4.38,
    4.09,
    2.52,
    5.19,
    2.39,
    3.66,
    2.29,
    2.88
])


# ============================================================
# MINOR KEY PROFILE
# ============================================================

MINOR_PROFILE = np.array([
    6.33,
    2.68,
    3.52,
    5.38,
    2.60,
    3.53,
    2.54,
    4.75,
    3.98,
    2.69,
    3.34,
    3.17
])


# ============================================================
# HEADER
# ============================================================

print("=" * 70)
print("AI MUSIC & AUDIO ANALYZER")
print("STEP 15 - KEY / CHROMA ANALYSIS")
print("=" * 70)


# ============================================================
# CHECK FILE
# ============================================================

if not os.path.exists(MUSIC_FILE):

    print("\n❌ Music file not found!")

    print(
        f"Expected: {MUSIC_FILE}"
    )

    exit()


# ============================================================
# CREATE REPORT DIRECTORY
# ============================================================

os.makedirs(
    REPORT_DIR,
    exist_ok=True
)


# ============================================================
# LOAD AUDIO
# ============================================================

try:

    audio, sample_rate = librosa.load(
        MUSIC_FILE,
        sr=None,
        mono=True
    )

    print(
        "\n✅ Music file loaded successfully."
    )

except Exception as error:

    print(
        "\n❌ Failed to load music file."
    )

    print(
        f"Error: {error}"
    )

    exit()


# ============================================================
# AUDIO INFORMATION
# ============================================================

samples = len(audio)

duration = (
    samples /
    sample_rate
)


print("\n" + "=" * 70)
print("AUDIO INFORMATION")
print("=" * 70)

print(
    f"Sample Rate : "
    f"{sample_rate} Hz"
)

print(
    f"Samples     : "
    f"{samples}"
)

print(
    f"Duration    : "
    f"{duration:.2f} sec"
)


# ============================================================
# CHROMA FEATURE
# ============================================================

print("\nCalculating chroma features...")

chroma = librosa.feature.chroma_stft(
    y=audio,
    sr=sample_rate,
    n_fft=4096,
    hop_length=512
)


# ============================================================
# AVERAGE CHROMA
# ============================================================

chroma_mean = np.mean(
    chroma,
    axis=1
)


# ============================================================
# NORMALIZE CHROMA
# ============================================================

if np.max(chroma_mean) > 0:

    chroma_normalized = (
        chroma_mean /
        np.max(chroma_mean)
    )

else:

    chroma_normalized = chroma_mean


# ============================================================
# DOMINANT NOTE
# ============================================================

dominant_note_index = np.argmax(
    chroma_mean
)

dominant_note = NOTE_NAMES[
    dominant_note_index
]

dominant_note_strength = (
    chroma_normalized[
        dominant_note_index
    ]
)


# ============================================================
# PRINT CHROMA PROFILE
# ============================================================

print("\n" + "=" * 70)
print("CHROMA PROFILE")
print("=" * 70)

for note, value in zip(
    NOTE_NAMES,
    chroma_normalized
):

    print(
        f"{note:<3} : "
        f"{value:.4f}"
    )


# ============================================================
# KEY ESTIMATION FUNCTION
# ============================================================

def rotate_profile(
    profile,
    root
):

    return np.roll(
        profile,
        root
    )


# ============================================================
# CALCULATE KEY CORRELATIONS
# ============================================================

key_results = []


for root in range(12):

    # Major key
    major_profile = rotate_profile(
        MAJOR_PROFILE,
        root
    )

    major_correlation = np.corrcoef(
        chroma_mean,
        major_profile
    )[0, 1]

    key_results.append(
        (
            major_correlation,
            NOTE_NAMES[root],
            "Major"
        )
    )


    # Minor key
    minor_profile = rotate_profile(
        MINOR_PROFILE,
        root
    )

    minor_correlation = np.corrcoef(
        chroma_mean,
        minor_profile
    )[0, 1]

    key_results.append(
        (
            minor_correlation,
            NOTE_NAMES[root],
            "Minor"
        )
    )


# ============================================================
# SORT RESULTS
# ============================================================

key_results.sort(
    reverse=True,
    key=lambda x: x[0]
)


# ============================================================
# BEST KEY
# ============================================================

best_correlation = (
    key_results[0][0]
)

estimated_key = (
    key_results[0][1]
    + " "
    + key_results[0][2]
)


# ============================================================
# SECOND BEST KEY
# ============================================================

second_best = key_results[1]

second_key = (
    second_best[1]
    + " "
    + second_best[2]
)

second_correlation = (
    second_best[0]
)


# ============================================================
# KEY CONFIDENCE
# ============================================================

confidence_difference = (
    best_correlation -
    second_correlation
)


if best_correlation >= 0.7:

    confidence = "High"

elif best_correlation >= 0.4:

    confidence = "Moderate"

elif best_correlation >= 0.2:

    confidence = "Low"

else:

    confidence = "Very Low"


# ============================================================
# KEY RESULTS
# ============================================================

print("\n" + "=" * 70)
print("KEY ESTIMATION")
print("=" * 70)

print(
    f"Estimated Key      : "
    f"{estimated_key}"
)

print(
    f"Correlation        : "
    f"{best_correlation:.4f}"
)

print(
    f"Second Best Key    : "
    f"{second_key}"
)

print(
    f"Second Correlation : "
    f"{second_correlation:.4f}"
)

print(
    f"Confidence Gap     : "
    f"{confidence_difference:.4f}"
)

print(
    f"Confidence         : "
    f"{confidence}"
)


# ============================================================
# TOP 5 KEY CANDIDATES
# ============================================================

print("\n" + "=" * 70)
print("TOP 5 KEY CANDIDATES")
print("=" * 70)

for index, result in enumerate(
    key_results[:5],
    start=1
):

    correlation, note, mode = result

    print(
        f"{index}. "
        f"{note} {mode:<6} "
        f"Correlation: "
        f"{correlation:.4f}"
    )


# ============================================================
# CHROMA VISUALIZATION
# ============================================================

fig = plt.figure(
    figsize=(14, 9)
)


# ============================================================
# CHROMA BAR GRAPH
# ============================================================

ax1 = plt.subplot2grid(
    (2, 1),
    (0, 0)
)


bars = ax1.bar(
    NOTE_NAMES,
    chroma_normalized
)


ax1.set_title(
    "Chroma / Pitch-Class Energy"
)

ax1.set_xlabel(
    "Musical Note"
)

ax1.set_ylabel(
    "Normalized Energy"
)

ax1.set_ylim(
    0,
    1.1
)

ax1.grid(
    axis="y",
    alpha=0.3
)


for bar, value in zip(
    bars,
    chroma_normalized
):

    ax1.text(
        bar.get_x()
        + bar.get_width() / 2,
        value + 0.02,
        f"{value:.2f}",
        ha="center",
        fontsize=8
    )


# ============================================================
# CHROMA OVER TIME
# ============================================================

ax2 = plt.subplot2grid(
    (2, 1),
    (1, 0)
)


img = librosa.display.specshow(
    chroma,
    x_axis="time",
    y_axis="chroma",
    sr=sample_rate,
    hop_length=512,
    ax=ax2
)


ax2.set_title(
    "Chroma Energy Over Time"
)

ax2.set_ylabel(
    "Pitch Class"
)

ax2.set_xlabel(
    "Time (seconds)"
)


fig.colorbar(
    img,
    ax=ax2
)


# ============================================================
# TITLE
# ============================================================

fig.suptitle(
    f"Music Key / Chroma Analysis — "
    f"Estimated Key: {estimated_key}",
    fontsize=16
)


plt.tight_layout(
    rect=[
        0,
        0,
        1,
        0.95
    ]
)


# ============================================================
# SAVE GRAPH
# ============================================================

plt.savefig(
    OUTPUT_FILE,
    dpi=160,
    bbox_inches="tight"
)


plt.show()


# ============================================================
# FINAL RESULT
# ============================================================

print("\n" + "=" * 70)
print("STEP 15 RESULT")
print("=" * 70)

print(
    "✅ Chroma features calculated."
)

print(
    "✅ 12 pitch classes analyzed."
)

print(
    "✅ Dominant musical note identified."
)

print(
    "✅ Major/minor key candidates calculated."
)

print(
    "✅ Estimated musical key generated."
)

print(
    "✅ Key confidence calculated."
)

print(
    "✅ Chroma visualization generated."
)

print(
    "\nSaved graph:"
)

print(
    f"   {OUTPUT_FILE}"
)

print("\n🎵 STEP 15 COMPLETE")