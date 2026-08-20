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
    "audio_quality_health_score.png"
)


# ============================================================
# HEADER
# ============================================================

print("=" * 70)
print("AI MUSIC & AUDIO ANALYZER")
print("STEP 17 - AUDIO QUALITY & HEALTH SCORE")
print("=" * 70)


# ============================================================
# CHECK FILE
# ============================================================

if not os.path.exists(MUSIC_FILE):

    print("\n❌ Music file not found!")
    print(f"Expected: {MUSIC_FILE}")
    exit()


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
# 1. SIGNAL LEVEL
# ============================================================

rms = np.sqrt(
    np.mean(audio ** 2)
)

peak = np.max(
    np.abs(audio)
)


rms_dbfs = (
    20 * np.log10(rms)
    if rms > 0
    else -120
)

peak_dbfs = (
    20 * np.log10(peak)
    if peak > 0
    else -120
)


# ============================================================
# 2. CLIPPING
# ============================================================

CLIPPING_THRESHOLD = 0.999


positive_clipped = np.sum(
    audio >= CLIPPING_THRESHOLD
)

negative_clipped = np.sum(
    audio <= -CLIPPING_THRESHOLD
)

total_clipped = (
    positive_clipped +
    negative_clipped
)


clipping_percentage = (
    total_clipped /
    samples
) * 100


# ============================================================
# 3. CREST FACTOR
# ============================================================

if rms > 0:

    crest_factor = (
        peak /
        rms
    )

else:

    crest_factor = 0


# ============================================================
# 4. DYNAMIC RANGE
# ============================================================

dynamic_range = (
    peak_dbfs -
    rms_dbfs
)


# ============================================================
# 5. SPECTRAL FEATURES
# ============================================================

spectral_centroid = (
    librosa.feature.spectral_centroid(
        y=audio,
        sr=sample_rate
    )[0]
)

spectral_bandwidth = (
    librosa.feature.spectral_bandwidth(
        y=audio,
        sr=sample_rate
    )[0]
)

spectral_rolloff = (
    librosa.feature.spectral_rolloff(
        y=audio,
        sr=sample_rate,
        roll_percent=0.85
    )[0]
)

spectral_flatness = (
    librosa.feature.spectral_flatness(
        y=audio
    )[0]
)

zcr = (
    librosa.feature.zero_crossing_rate(
        audio
    )[0]
)


centroid_mean = np.mean(
    spectral_centroid
)

bandwidth_mean = np.mean(
    spectral_bandwidth
)

rolloff_mean = np.mean(
    spectral_rolloff
)

flatness_mean = np.mean(
    spectral_flatness
)

zcr_mean = np.mean(
    zcr
)


# ============================================================
# 6. BASS / MID / TREBLE
# ============================================================

N_FFT = 2048

HOP_LENGTH = 512


stft = librosa.stft(
    audio,
    n_fft=N_FFT,
    hop_length=HOP_LENGTH
)


frequencies = librosa.fft_frequencies(
    sr=sample_rate,
    n_fft=N_FFT
)


magnitude = np.abs(
    stft
)


bass_mask = (
    (frequencies >= 20) &
    (frequencies < 250)
)

mid_mask = (
    (frequencies >= 250) &
    (frequencies < 4000)
)

treble_mask = (
    (frequencies >= 4000) &
    (frequencies <= 20000)
)


bass_energy = np.mean(
    magnitude[bass_mask] ** 2
)

mid_energy = np.mean(
    magnitude[mid_mask] ** 2
)

treble_energy = np.mean(
    magnitude[treble_mask] ** 2
)


total_energy = (
    bass_energy +
    mid_energy +
    treble_energy
)


if total_energy > 0:

    bass_percent = (
        bass_energy /
        total_energy
    ) * 100

    mid_percent = (
        mid_energy /
        total_energy
    ) * 100

    treble_percent = (
        treble_energy /
        total_energy
    ) * 100

else:

    bass_percent = 0
    mid_percent = 0
    treble_percent = 0


# ============================================================
# 7. TEMPO
# ============================================================

onset_envelope = (
    librosa.onset.onset_strength(
        y=audio,
        sr=sample_rate
    )
)


tempo, beat_frames = (
    librosa.beat.beat_track(
        onset_envelope=onset_envelope,
        sr=sample_rate
    )
)


tempo_value = float(
    np.asarray(
        tempo
    ).flatten()[0]
)


beat_count = len(
    beat_frames
)


# ============================================================
# 8. KEY / CHROMA
# ============================================================

chroma = librosa.feature.chroma_stft(
    y=audio,
    sr=sample_rate,
    n_fft=4096,
    hop_length=512
)


chroma_mean = np.mean(
    chroma,
    axis=1
)


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


def rotate_profile(
    profile,
    root
):

    return np.roll(
        profile,
        root
    )


key_results = []


for root in range(12):

    major_profile = rotate_profile(
        MAJOR_PROFILE,
        root
    )

    major_corr = np.corrcoef(
        chroma_mean,
        major_profile
    )[0, 1]

    key_results.append(
        (
            major_corr,
            NOTE_NAMES[root],
            "Major"
        )
    )


    minor_profile = rotate_profile(
        MINOR_PROFILE,
        root
    )

    minor_corr = np.corrcoef(
        chroma_mean,
        minor_profile
    )[0, 1]

    key_results.append(
        (
            minor_corr,
            NOTE_NAMES[root],
            "Minor"
        )
    )


key_results.sort(
    reverse=True,
    key=lambda x: x[0]
)


best_key_corr = (
    key_results[0][0]
)

best_key = (
    key_results[0][1]
    + " "
    + key_results[0][2]
)


second_key_corr = (
    key_results[1][0]
)


key_gap = (
    best_key_corr -
    second_key_corr
)


# ============================================================
# SCORE 1 — SIGNAL LEVEL
# MAX 20
# ============================================================

signal_score = 0


if -24 <= rms_dbfs <= -10:

    signal_score = 20

elif -30 <= rms_dbfs < -24:

    signal_score = 15

elif -10 < rms_dbfs <= -6:

    signal_score = 15

elif rms_dbfs < -30:

    signal_score = 10

else:

    signal_score = 8


# ============================================================
# SCORE 2 — CLIPPING
# MAX 20
# ============================================================

if total_clipped == 0:

    clipping_score = 20

elif clipping_percentage < 0.001:

    clipping_score = 15

elif clipping_percentage < 0.01:

    clipping_score = 10

else:

    clipping_score = 0


# ============================================================
# SCORE 3 — DYNAMIC CHARACTERISTICS
# MAX 15
# ============================================================

if 8 <= dynamic_range <= 20:

    dynamic_score = 15

elif 5 <= dynamic_range < 8:

    dynamic_score = 11

elif 20 < dynamic_range <= 30:

    dynamic_score = 12

else:

    dynamic_score = 7


# ============================================================
# SCORE 4 — FREQUENCY BALANCE
# MAX 15
# ============================================================

# Avoid treating extreme bass dominance as automatically bad.
# Score is based on whether all three regions contain measurable
# energy.

active_bands = sum([
    bass_percent > 1,
    mid_percent > 1,
    treble_percent > 1
])


if active_bands == 3:

    balance_score = 15

elif active_bands == 2:

    balance_score = 11

elif active_bands == 1:

    balance_score = 7

else:

    balance_score = 3


# ============================================================
# SCORE 5 — SPECTRAL QUALITY
# MAX 10
# ============================================================

spectral_score = 0


if (
    centroid_mean > 500 and
    bandwidth_mean > 500 and
    rolloff_mean > 1000
):

    spectral_score = 10

elif centroid_mean > 300:

    spectral_score = 7

else:

    spectral_score = 4


# ============================================================
# SCORE 6 — RHYTHM
# MAX 10
# ============================================================

if 60 <= tempo_value <= 180 and beat_count >= 10:

    rhythm_score = 10

elif beat_count >= 5:

    rhythm_score = 7

else:

    rhythm_score = 4


# ============================================================
# SCORE 7 — KEY / CHROMA
# MAX 10
# ============================================================

if best_key_corr >= 0.70:

    key_score = 10

elif best_key_corr >= 0.50:

    key_score = 8

elif best_key_corr >= 0.30:

    key_score = 6

else:

    key_score = 3


# ============================================================
# TOTAL SCORE
# ============================================================

total_score = (
    signal_score +
    clipping_score +
    dynamic_score +
    balance_score +
    spectral_score +
    rhythm_score +
    key_score
)


# ============================================================
# HEALTH CLASSIFICATION
# ============================================================

if total_score >= 90:

    health = "Excellent"

elif total_score >= 75:

    health = "Good"

elif total_score >= 60:

    health = "Fair"

else:

    health = "Needs Attention"


# ============================================================
# PRINT RESULTS
# ============================================================

print("\n" + "=" * 70)
print("AUDIO QUALITY SCORE")
print("=" * 70)

print(
    f"Signal Level Score     : "
    f"{signal_score}/20"
)

print(
    f"Clipping Safety Score  : "
    f"{clipping_score}/20"
)

print(
    f"Dynamic Score          : "
    f"{dynamic_score}/15"
)

print(
    f"Frequency Balance      : "
    f"{balance_score}/15"
)

print(
    f"Spectral Quality       : "
    f"{spectral_score}/10"
)

print(
    f"Rhythm Score           : "
    f"{rhythm_score}/10"
)

print(
    f"Key / Chroma Score     : "
    f"{key_score}/10"
)


print("\n" + "=" * 70)
print("FINAL AUDIO HEALTH")
print("=" * 70)

print(
    f"Total Score            : "
    f"{total_score}/100"
)

print(
    f"Health Classification  : "
    f"{health}"
)


print("\n" + "=" * 70)
print("KEY PROJECT FINDINGS")
print("=" * 70)

print(
    f"Estimated Key          : "
    f"{best_key}"
)

print(
    f"Key Correlation        : "
    f"{best_key_corr:.4f}"
)

print(
    f"Estimated BPM          : "
    f"{tempo_value:.2f}"
)

print(
    f"Dominant Band          : "
    f"Bass ({bass_percent:.2f}%)"
)

print(
    f"Clipping               : "
    f"{total_clipped} samples"
)

print(
    f"Peak Level             : "
    f"{peak_dbfs:.2f} dBFS"
)

print(
    f"Dynamic Range          : "
    f"{dynamic_range:.2f} dB"
)


# ============================================================
# VISUALIZATION
# ============================================================

fig = plt.figure(
    figsize=(14, 9)
)


# ============================================================
# SCORE BAR
# ============================================================

ax1 = plt.subplot2grid(
    (2, 2),
    (0, 0),
    colspan=2
)


ax1.barh(
    ["Audio Health"],
    [total_score]
)

ax1.set_xlim(
    0,
    100
)

ax1.set_xlabel(
    "Score"
)

ax1.set_title(
    f"Overall Audio Health Score: "
    f"{total_score}/100 — {health}"
)

ax1.grid(
    axis="x",
    alpha=0.3
)


ax1.text(
    total_score + 1,
    0,
    f"{total_score}/100",
    va="center",
    fontweight="bold"
)


# ============================================================
# COMPONENT SCORES
# ============================================================

ax2 = plt.subplot2grid(
    (2, 2),
    (1, 0)
)


component_names = [
    "Signal",
    "Clipping",
    "Dynamic",
    "Balance",
    "Spectral",
    "Rhythm",
    "Key"
]


component_scores = [
    signal_score,
    clipping_score,
    dynamic_score,
    balance_score,
    spectral_score,
    rhythm_score,
    key_score
]


component_max = [
    20,
    20,
    15,
    15,
    10,
    10,
    10
]


component_percent = [
    score / maximum * 100
    for score, maximum in zip(
        component_scores,
        component_max
    )
]


bars = ax2.barh(
    component_names,
    component_percent
)

ax2.set_xlim(
    0,
    100
)

ax2.invert_yaxis()

ax2.set_xlabel(
    "Component Score (%)"
)

ax2.set_title(
    "Quality Score Breakdown"
)

ax2.grid(
    axis="x",
    alpha=0.3
)


for bar, value in zip(
    bars,
    component_percent
):

    ax2.text(
        value + 1,
        bar.get_y()
        + bar.get_height() / 2,
        f"{value:.0f}%",
        va="center",
        fontsize=8
    )


# ============================================================
# SUMMARY PANEL
# ============================================================

ax3 = plt.subplot2grid(
    (2, 2),
    (1, 1)
)

ax3.axis(
    "off"
)


summary = (
    "AUDIO QUALITY SUMMARY\n"
    "────────────────────────────\n"
    f"Health       : {health}\n"
    f"Score        : {total_score}/100\n\n"
    f"RMS          : {rms_dbfs:.2f} dBFS\n"
    f"Peak         : {peak_dbfs:.2f} dBFS\n"
    f"Dynamic      : {dynamic_range:.2f} dB\n"
    f"Clipping     : {total_clipped}\n\n"
    f"BPM          : {tempo_value:.2f}\n"
    f"Key          : {best_key}\n"
    f"Key Corr.    : {best_key_corr:.4f}\n\n"
    f"Bass         : {bass_percent:.2f}%\n"
    f"Mid          : {mid_percent:.2f}%\n"
    f"Treble       : {treble_percent:.2f}%"
)


ax3.text(
    0.05,
    0.95,
    summary,
    transform=ax3.transAxes,
    fontsize=11,
    family="monospace",
    verticalalignment="top"
)


# ============================================================
# FIGURE TITLE
# ============================================================

fig.suptitle(
    "AI Music & Audio Analyzer — Audio Quality & Health",
    fontsize=17
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
# SAVE
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
print("STEP 17 RESULT")
print("=" * 70)

print(
    "✅ Signal quality score calculated."
)

print(
    "✅ Clipping safety score calculated."
)

print(
    "✅ Dynamic characteristics scored."
)

print(
    "✅ Frequency balance scored."
)

print(
    "✅ Spectral quality scored."
)

print(
    "✅ Rhythm score calculated."
)

print(
    "✅ Key/chroma score calculated."
)

print(
    "✅ Overall audio health score generated."
)

print(
    "✅ Quality visualization generated."
)

print("\nSaved report:")

print(
    f"   {OUTPUT_FILE}"
)

print("\n🎵 STEP 17 COMPLETE")