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
    "music_loudness_dynamic_range.png"
)


# ============================================================
# HEADER
# ============================================================

print("=" * 70)
print("AI MUSIC & AUDIO ANALYZER")
print("STEP 16 - LOUDNESS / DYNAMIC RANGE / CLIPPING ANALYSIS")
print("=" * 70)


# ============================================================
# CHECK FILE
# ============================================================

if not os.path.exists(MUSIC_FILE):

    print("\n❌ Music file not found!")
    print(f"Expected: {MUSIC_FILE}")
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

    print("\n✅ Music file loaded successfully.")

except Exception as error:

    print("\n❌ Failed to load music file.")
    print(f"Error: {error}")
    exit()


# ============================================================
# BASIC INFORMATION
# ============================================================

samples = len(audio)

duration = samples / sample_rate


print("\n" + "=" * 70)
print("AUDIO INFORMATION")
print("=" * 70)

print(
    f"Sample Rate : {sample_rate} Hz"
)

print(
    f"Samples     : {samples}"
)

print(
    f"Duration    : {duration:.2f} sec"
)


# ============================================================
# RMS
# ============================================================

rms = np.sqrt(
    np.mean(audio ** 2)
)


rms_dbfs = (
    20 * np.log10(rms)
    if rms > 0
    else float("-inf")
)


# ============================================================
# PEAK
# ============================================================

peak = np.max(
    np.abs(audio)
)


peak_dbfs = (
    20 * np.log10(peak)
    if peak > 0
    else float("-inf")
)


# ============================================================
# CREST FACTOR
# ============================================================

if rms > 0:

    crest_factor = (
        peak /
        rms
    )

else:

    crest_factor = 0


# ============================================================
# DYNAMIC RANGE
# ============================================================

dynamic_range = (
    peak_dbfs -
    rms_dbfs
)


# ============================================================
# CLIPPING ANALYSIS
# ============================================================

# Digital clipping threshold
# Samples at or extremely close to full scale.

CLIPPING_THRESHOLD = 0.999


clipped_positive = np.sum(
    audio >= CLIPPING_THRESHOLD
)

clipped_negative = np.sum(
    audio <= -CLIPPING_THRESHOLD
)


total_clipped = (
    clipped_positive +
    clipped_negative
)


clipping_percentage = (
    total_clipped /
    samples
) * 100


# ============================================================
# CLIPPING STATUS
# ============================================================

if total_clipped == 0:

    clipping_status = "No Clipping Detected"

elif clipping_percentage < 0.01:

    clipping_status = "Very Low Clipping"

elif clipping_percentage < 0.1:

    clipping_status = "Low Clipping"

else:

    clipping_status = "Significant Clipping"


# ============================================================
# SHORT-TERM RMS
# ============================================================

FRAME_LENGTH = 4096

HOP_LENGTH = 2048


rms_frames = librosa.feature.rms(
    y=audio,
    frame_length=FRAME_LENGTH,
    hop_length=HOP_LENGTH
)[0]


rms_db_frames = (
    20 *
    np.log10(
        np.maximum(
            rms_frames,
            1e-10
        )
    )
)


rms_time = librosa.frames_to_time(
    np.arange(
        len(rms_db_frames)
    ),
    sr=sample_rate,
    hop_length=HOP_LENGTH
)


# ============================================================
# LOUDNESS STATISTICS
# ============================================================

short_term_average = np.mean(
    rms_db_frames
)

short_term_maximum = np.max(
    rms_db_frames
)

short_term_minimum = np.min(
    rms_db_frames
)


loudness_range = (
    short_term_maximum -
    short_term_minimum
)


# ============================================================
# PRINT SIGNAL RESULTS
# ============================================================

print("\n" + "=" * 70)
print("LOUDNESS RESULTS")
print("=" * 70)

print(
    f"RMS Amplitude       : "
    f"{rms:.6f}"
)

print(
    f"RMS Level           : "
    f"{rms_dbfs:.2f} dBFS"
)

print(
    f"Peak Amplitude      : "
    f"{peak:.6f}"
)

print(
    f"Peak Level          : "
    f"{peak_dbfs:.2f} dBFS"
)

print(
    f"Crest Factor        : "
    f"{crest_factor:.3f}"
)

print(
    f"Dynamic Range       : "
    f"{dynamic_range:.2f} dB"
)


# ============================================================
# PRINT SHORT-TERM RESULTS
# ============================================================

print("\n" + "=" * 70)
print("LOUDNESS OVER TIME")
print("=" * 70)

print(
    f"Average RMS Level   : "
    f"{short_term_average:.2f} dBFS"
)

print(
    f"Maximum RMS Level   : "
    f"{short_term_maximum:.2f} dBFS"
)

print(
    f"Minimum RMS Level   : "
    f"{short_term_minimum:.2f} dBFS"
)

print(
    f"Loudness Variation  : "
    f"{loudness_range:.2f} dB"
)


# ============================================================
# PRINT CLIPPING RESULTS
# ============================================================

print("\n" + "=" * 70)
print("CLIPPING ANALYSIS")
print("=" * 70)

print(
    f"Clipping Threshold  : "
    f"{CLIPPING_THRESHOLD}"
)

print(
    f"Positive Clipped    : "
    f"{clipped_positive}"
)

print(
    f"Negative Clipped    : "
    f"{clipped_negative}"
)

print(
    f"Total Clipped       : "
    f"{total_clipped}"
)

print(
    f"Clipping Percentage : "
    f"{clipping_percentage:.6f}%"
)

print(
    f"Clipping Status     : "
    f"{clipping_status}"
)


# ============================================================
# CREATE VISUALIZATION
# ============================================================

fig, axes = plt.subplots(
    2,
    1,
    figsize=(14, 8)
)


# ============================================================
# RMS LOUDNESS GRAPH
# ============================================================

axes[0].plot(
    rms_time,
    rms_db_frames
)

axes[0].axhline(
    rms_dbfs,
    linestyle="--",
    label=f"Average RMS: {rms_dbfs:.2f} dBFS"
)

axes[0].set_title(
    "RMS Loudness Over Time"
)

axes[0].set_xlabel(
    "Time (seconds)"
)

axes[0].set_ylabel(
    "Level (dBFS)"
)

axes[0].grid(
    True,
    alpha=0.3
)

axes[0].legend()


# ============================================================
# AUDIO PEAK VIEW
# ============================================================

time = np.arange(
    samples
) / sample_rate


# Downsample for visualization
plot_step = max(
    1,
    samples // 200000
)


axes[1].plot(
    time[::plot_step],
    audio[::plot_step],
    alpha=0.8
)


axes[1].axhline(
    CLIPPING_THRESHOLD,
    linestyle="--",
    label="Clipping Threshold"
)

axes[1].axhline(
    -CLIPPING_THRESHOLD,
    linestyle="--"
)


axes[1].set_title(
    "Audio Peak / Clipping View"
)

axes[1].set_xlabel(
    "Time (seconds)"
)

axes[1].set_ylabel(
    "Amplitude"
)

axes[1].grid(
    True,
    alpha=0.3
)

axes[1].legend()


# ============================================================
# TITLE
# ============================================================

fig.suptitle(
    "Music Loudness, Dynamic Range & Clipping Analysis",
    fontsize=16
)


plt.tight_layout(
    rect=[
        0,
        0,
        1,
        0.96
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
print("STEP 16 RESULT")
print("=" * 70)

print(
    "✅ RMS loudness calculated."
)

print(
    "✅ Peak level calculated."
)

print(
    "✅ Crest factor calculated."
)

print(
    "✅ Dynamic range calculated."
)

print(
    "✅ Short-term loudness analyzed."
)

print(
    "✅ Clipping samples detected."
)

print(
    "✅ Clipping percentage calculated."
)

print(
    "✅ Loudness visualization generated."
)

print("\nSaved graph:")

print(
    f"   {OUTPUT_FILE}"
)

print("\n🎵 STEP 16 COMPLETE")