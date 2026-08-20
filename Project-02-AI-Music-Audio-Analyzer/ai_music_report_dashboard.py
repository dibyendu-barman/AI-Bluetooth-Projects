import json
import os

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle


# ============================================================
# CONFIGURATION
# ============================================================

FEATURE_FILE = os.path.join(
    "reports",
    "music_feature_summary.json"
)

AI_FILE = os.path.join(
    "reports",
    "music_ai_interpretation.json"
)

OUTPUT_FILE = os.path.join(
    "reports",
    "ai_music_analysis_dashboard.png"
)


# ============================================================
# HEADER
# ============================================================

print("=" * 70)
print("AI MUSIC & AUDIO ANALYZER")
print("STEP 18C - AI MUSIC REPORT & DASHBOARD")
print("=" * 70)


# ============================================================
# CHECK FILES
# ============================================================

if not os.path.exists(FEATURE_FILE):

    print("\n❌ Feature summary not found.")
    print(
        "Run: python .\\music_feature_summary.py"
    )
    exit()


if not os.path.exists(AI_FILE):

    print("\n❌ AI interpretation not found.")
    print(
        "Run: python .\\ai_music_understanding.py"
    )
    exit()


print("\n✅ Feature summary found.")
print("✅ AI interpretation found.")


# ============================================================
# LOAD JSON FILES
# ============================================================

try:

    with open(
        FEATURE_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        features = json.load(file)

    with open(
        AI_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        ai_data = json.load(file)

    print("✅ Analysis data loaded successfully.")

except Exception as error:

    print("\n❌ Failed to load analysis data.")
    print(f"Error: {error}")
    exit()


# ============================================================
# EXTRACT FEATURE DATA
# ============================================================

file_info = features["file"]
signal = features["signal"]
clipping = features["clipping"]
spectral = features["spectral"]
frequency = features["frequency_balance"]
rhythm = features["rhythm"]
music = features["music"]
quality = features["quality"]

ai = ai_data["ai_interpretation"]


# ============================================================
# VALUES
# ============================================================

track_name = file_info["name"]

duration = file_info["duration_sec"]

sample_rate = file_info["sample_rate_hz"]

channels = file_info["channels"]

rms_dbfs = signal["rms_dbfs"]

peak_dbfs = signal["peak_dbfs"]

dynamic_range = signal["dynamic_range_db"]

crest_factor = signal["crest_factor"]

bass = frequency["bass_percent"]

mid = frequency["mid_percent"]

treble = frequency["treble_percent"]

dominant_band = frequency["dominant_band"]

bpm = rhythm["bpm"]

tempo_category = rhythm["tempo_category"]

beats = rhythm["beats"]

onsets = rhythm["onsets"]

estimated_key = music["estimated_key"]

key_correlation = music["key_correlation"]

centroid = spectral["centroid_hz"]

bandwidth = spectral["bandwidth_hz"]

rolloff = spectral["rolloff_hz"]

flatness = spectral["flatness"]

zcr = spectral["zero_crossing_rate"]

health_score = quality["health_score"]

health_classification = quality["classification"]

clipped_samples = clipping["clipped_samples"]

clipping_percentage = clipping["clipping_percentage"]


# ============================================================
# CONSOLE SUMMARY
# ============================================================

print("\n" + "=" * 70)
print("AI MUSIC REPORT DATA")
print("=" * 70)

print(f"\nTrack             : {track_name}")
print(f"Duration          : {duration:.2f} sec")
print(f"Sample Rate       : {sample_rate} Hz")
print(f"Channels          : {channels}")

print(f"\nEstimated Key     : {estimated_key}")
print(f"Key Correlation   : {key_correlation:.4f}")

print(f"\nBPM               : {bpm:.2f}")
print(f"Tempo Category    : {tempo_category}")

print(f"\nDominant Band     : {dominant_band}")

print(
    f"Bass / Mid / Treble : "
    f"{bass:.2f}% / "
    f"{mid:.2f}% / "
    f"{treble:.2f}%"
)

print(f"\nRMS Level         : {rms_dbfs:.2f} dBFS")
print(f"Peak Level        : {peak_dbfs:.2f} dBFS")
print(f"Dynamic Range     : {dynamic_range:.2f} dB")

print(f"\nClipping Samples  : {clipped_samples}")
print(f"Health Score      : {health_score}/100")
print(f"Classification    : {health_classification}")


# ============================================================
# CREATE DASHBOARD
# ============================================================

fig = plt.figure(
    figsize=(18, 11)
)

fig.patch.set_facecolor(
    "#F4F6F8"
)


# ============================================================
# TITLE
# ============================================================

fig.text(
    0.05,
    0.965,
    "AI MUSIC & AUDIO ANALYZER",
    fontsize=25,
    fontweight="bold"
)

fig.text(
    0.05,
    0.935,
    "AI-Powered Music Analysis Dashboard • Step 18C",
    fontsize=12
)

fig.text(
    0.95,
    0.955,
    "v1.0",
    fontsize=13,
    fontweight="bold",
    ha="right"
)


# ============================================================
# TRACK INFORMATION PANEL
# ============================================================

ax_info = fig.add_axes(
    [0.05, 0.78, 0.90, 0.12]
)

ax_info.axis("off")

ax_info.add_patch(
    Rectangle(
        (0, 0),
        1,
        1,
        transform=ax_info.transAxes,
        linewidth=0.8,
        edgecolor="#D0D5D9",
        facecolor="white"
    )
)

ax_info.text(
    0.02,
    0.72,
    "TRACK",
    fontsize=9,
    fontweight="bold"
)

ax_info.text(
    0.02,
    0.43,
    track_name,
    fontsize=14,
    fontweight="bold"
)

ax_info.text(
    0.30,
    0.72,
    "DURATION",
    fontsize=9,
    fontweight="bold"
)

ax_info.text(
    0.30,
    0.43,
    f"{duration:.2f} sec",
    fontsize=14
)

ax_info.text(
    0.48,
    0.72,
    "SAMPLE RATE",
    fontsize=9,
    fontweight="bold"
)

ax_info.text(
    0.48,
    0.43,
    f"{sample_rate:,} Hz",
    fontsize=14
)

ax_info.text(
    0.68,
    0.72,
    "KEY",
    fontsize=9,
    fontweight="bold"
)

ax_info.text(
    0.68,
    0.43,
    estimated_key,
    fontsize=14,
    fontweight="bold"
)

ax_info.text(
    0.84,
    0.72,
    "BPM",
    fontsize=9,
    fontweight="bold"
)

ax_info.text(
    0.84,
    0.43,
    f"{bpm:.2f}",
    fontsize=14,
    fontweight="bold"
)


# ============================================================
# HEALTH SCORE
# ============================================================

ax_score = fig.add_axes(
    [0.05, 0.59, 0.20, 0.14]
)

ax_score.axis("off")

ax_score.add_patch(
    Rectangle(
        (0, 0),
        1,
        1,
        transform=ax_score.transAxes,
        linewidth=0.8,
        edgecolor="#D0D5D9",
        facecolor="white"
    )
)

ax_score.text(
    0.50,
    0.78,
    "AUDIO HEALTH",
    ha="center",
    fontsize=10,
    fontweight="bold"
)

ax_score.text(
    0.50,
    0.42,
    f"{health_score}/100",
    ha="center",
    fontsize=28,
    fontweight="bold"
)

ax_score.text(
    0.50,
    0.15,
    health_classification,
    ha="center",
    fontsize=12
)


# ============================================================
# RHYTHM PANEL
# ============================================================

ax_rhythm = fig.add_axes(
    [0.27, 0.59, 0.20, 0.14]
)

ax_rhythm.axis("off")

ax_rhythm.add_patch(
    Rectangle(
        (0, 0),
        1,
        1,
        transform=ax_rhythm.transAxes,
        linewidth=0.8,
        edgecolor="#D0D5D9",
        facecolor="white"
    )
)

ax_rhythm.text(
    0.05,
    0.78,
    "RHYTHM",
    fontsize=10,
    fontweight="bold"
)

ax_rhythm.text(
    0.05,
    0.48,
    f"{bpm:.2f} BPM",
    fontsize=22,
    fontweight="bold"
)

ax_rhythm.text(
    0.05,
    0.25,
    f"{tempo_category} • "
    f"{beats} beats • "
    f"{onsets} onsets",
    fontsize=9
)


# ============================================================
# SIGNAL PANEL
# ============================================================

ax_signal = fig.add_axes(
    [0.49, 0.59, 0.20, 0.14]
)

ax_signal.axis("off")

ax_signal.add_patch(
    Rectangle(
        (0, 0),
        1,
        1,
        transform=ax_signal.transAxes,
        linewidth=0.8,
        edgecolor="#D0D5D9",
        facecolor="white"
    )
)

ax_signal.text(
    0.05,
    0.78,
    "SIGNAL",
    fontsize=10,
    fontweight="bold"
)

ax_signal.text(
    0.05,
    0.50,
    f"RMS {rms_dbfs:.2f} dBFS",
    fontsize=13
)

ax_signal.text(
    0.05,
    0.28,
    f"Peak {peak_dbfs:.2f} dBFS",
    fontsize=13
)

ax_signal.text(
    0.05,
    0.08,
    f"Dynamic {dynamic_range:.2f} dB",
    fontsize=9
)


# ============================================================
# CLIPPING PANEL
# ============================================================

ax_clip = fig.add_axes(
    [0.71, 0.59, 0.24, 0.14]
)

ax_clip.axis("off")

ax_clip.add_patch(
    Rectangle(
        (0, 0),
        1,
        1,
        transform=ax_clip.transAxes,
        linewidth=0.8,
        edgecolor="#D0D5D9",
        facecolor="white"
    )
)

ax_clip.text(
    0.05,
    0.78,
    "CLIPPING",
    fontsize=10,
    fontweight="bold"
)

ax_clip.text(
    0.05,
    0.47,
    f"{clipped_samples} samples",
    fontsize=21,
    fontweight="bold"
)

ax_clip.text(
    0.05,
    0.20,
    f"{clipping_percentage:.6f}%",
    fontsize=11
)

ax_clip.text(
    0.55,
    0.20,
    "No Clipping Detected",
    fontsize=9
)


# ============================================================
# FREQUENCY BAR CHART
# ============================================================

ax_freq = fig.add_axes(
    [0.05, 0.32, 0.42, 0.20]
)

bands = [
    "Bass",
    "Mid",
    "Treble"
]

values = [
    bass,
    mid,
    treble
]

bars = ax_freq.bar(
    bands,
    values
)

ax_freq.set_title(
    "Frequency Energy Distribution",
    loc="left",
    fontweight="bold"
)

ax_freq.set_ylabel(
    "Energy (%)"
)

ax_freq.set_ylim(
    0,
    100
)

for bar, value in zip(
    bars,
    values
):

    ax_freq.text(
        bar.get_x()
        + bar.get_width() / 2,
        value + 1,
        f"{value:.2f}%",
        ha="center",
        fontsize=9
    )


# ============================================================
# SPECTRAL FEATURES
# ============================================================

ax_spec = fig.add_axes(
    [0.53, 0.32, 0.42, 0.20]
)

ax_spec.axis("off")

ax_spec.add_patch(
    Rectangle(
        (0, 0),
        1,
        1,
        transform=ax_spec.transAxes,
        linewidth=0.8,
        edgecolor="#D0D5D9",
        facecolor="white"
    )
)

ax_spec.text(
    0.03,
    0.90,
    "SPECTRAL CHARACTERISTICS",
    fontsize=11,
    fontweight="bold"
)

spec_lines = [
    f"Centroid       : {centroid:.2f} Hz",
    f"Bandwidth      : {bandwidth:.2f} Hz",
    f"Rolloff        : {rolloff:.2f} Hz",
    f"Flatness       : {flatness:.6f}",
    f"Zero Crossing  : {zcr:.6f}",
    f"Dominant Band  : {dominant_band}"
]

for index, line in enumerate(
    spec_lines
):

    ax_spec.text(
        0.03,
        0.72 - index * 0.12,
        line,
        fontsize=10
    )


# ============================================================
# AI INTERPRETATION PANEL
# ============================================================

ax_ai = fig.add_axes(
    [0.05, 0.05, 0.90, 0.22]
)

ax_ai.axis("off")

ax_ai.add_patch(
    Rectangle(
        (0, 0),
        1,
        1,
        transform=ax_ai.transAxes,
        linewidth=0.8,
        edgecolor="#D0D5D9",
        facecolor="white"
    )
)

ax_ai.text(
    0.02,
    0.90,
    "AI MUSIC INTERPRETATION",
    fontsize=13,
    fontweight="bold"
)

summary = ai.get(
    "overall_interpretation",
    ""
)

findings = ai.get(
    "important_findings",
    []
)

summary_text = (
    summary[:700]
    + ("..." if len(summary) > 700 else "")
)

ax_ai.text(
    0.02,
    0.68,
    summary_text,
    fontsize=9.5,
    verticalalignment="top",
    wrap=True
)

ax_ai.text(
    0.02,
    0.27,
    "KEY FINDINGS",
    fontsize=10,
    fontweight="bold"
)

finding_text = " • ".join(
    str(item)
    for item in findings[:3]
)

ax_ai.text(
    0.02,
    0.10,
    finding_text[:550],
    fontsize=9,
    verticalalignment="bottom",
    wrap=True
)


# ============================================================
# FOOTER
# ============================================================

fig.text(
    0.05,
    0.015,
    "AI Music & Audio Analyzer • Step 18C • "
    "DSP measurements + Gemini AI interpretation",
    fontsize=8
)

fig.text(
    0.95,
    0.015,
    "Project v1.0",
    fontsize=8,
    ha="right"
)


# ============================================================
# SAVE
# ============================================================

plt.savefig(
    OUTPUT_FILE,
    dpi=180,
    bbox_inches="tight"
)

plt.close()


# ============================================================
# FINAL RESULT
# ============================================================

print("\n" + "=" * 70)
print("STEP 18C RESULT")
print("=" * 70)

print(
    "✅ DSP feature data integrated."
)

print(
    "✅ Audio health score integrated."
)

print(
    "✅ Key and BPM integrated."
)

print(
    "✅ Frequency distribution integrated."
)

print(
    "✅ Spectral features integrated."
)

print(
    "✅ Clipping analysis integrated."
)

print(
    "✅ Gemini AI interpretation integrated."
)

print(
    "✅ AI findings integrated."
)

print(
    "✅ Professional dashboard generated."
)

print("\nSaved dashboard:")

print(
    f"   {OUTPUT_FILE}"
)

print("\n🎵 STEP 18C COMPLETE")