import librosa
import librosa.display
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
    "music_analysis_dashboard_v2.png"
)


# ============================================================
# HEADER
# ============================================================

print("=" * 70)
print("AI MUSIC & AUDIO ANALYZER")
print("STEP 14 - PROFESSIONAL MUSIC ANALYSIS DASHBOARD")
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


# ============================================================
# SIGNAL LEVEL
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
    else float("-inf")
)

peak_dbfs = (
    20 * np.log10(peak)
    if peak > 0
    else float("-inf")
)


# ============================================================
# FFT
# ============================================================

window = np.hanning(
    len(audio)
)

windowed_audio = audio * window

fft_result = np.fft.rfft(
    windowed_audio
)

fft_magnitude = np.abs(
    fft_result
)

fft_magnitude = (
    fft_magnitude /
    len(audio)
)

fft_frequencies = np.fft.rfftfreq(
    len(audio),
    d=1 / sample_rate
)


# ============================================================
# SPECTRAL FEATURES
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
# STFT
# ============================================================

N_FFT = 2048

HOP_LENGTH = 512


stft = librosa.stft(
    audio,
    n_fft=N_FFT,
    hop_length=HOP_LENGTH
)

spectrogram_db = librosa.amplitude_to_db(
    np.abs(stft),
    ref=np.max
)


# ============================================================
# BASS / MID / TREBLE
# ============================================================

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


bands = {
    "Bass": bass_percent,
    "Mid": mid_percent,
    "Treble": treble_percent
}

dominant_band = max(
    bands,
    key=bands.get
)


# ============================================================
# TEMPO / BEAT ANALYSIS
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


beat_times = librosa.frames_to_time(
    beat_frames,
    sr=sample_rate
)


# ============================================================
# HUMAN-READABLE DURATION
# ============================================================

minutes = int(
    duration // 60
)

seconds = int(
    duration % 60
)

duration_text = (
    f"{minutes}:{seconds:02d}"
)


# ============================================================
# CREATE DASHBOARD
# ============================================================

fig = plt.figure(
    figsize=(16, 12)
)

fig.patch.set_facecolor(
    "#111827"
)


# ============================================================
# TITLE
# ============================================================

fig.text(
    0.05,
    0.965,
    "AI MUSIC & AUDIO ANALYZER",
    fontsize=24,
    fontweight="bold",
    color="white"
)

fig.text(
    0.05,
    0.935,
    f"{os.path.basename(MUSIC_FILE)}  •  "
    f"{duration_text}  •  "
    f"{sample_rate / 1000:.1f} kHz  •  Mono",
    fontsize=11,
    color="#CBD5E1"
)


# ============================================================
# KPI CARD FUNCTION
# ============================================================

def add_kpi(
    x,
    value,
    label
):

    fig.text(
        x,
        0.875,
        value,
        fontsize=22,
        fontweight="bold",
        color="white",
        ha="center"
    )

    fig.text(
        x,
        0.845,
        label,
        fontsize=10,
        color="#94A3B8",
        ha="center"
    )


# ============================================================
# KPI CARDS
# ============================================================

add_kpi(
    0.15,
    f"{tempo_value:.2f}",
    "BPM"
)

add_kpi(
    0.35,
    f"{rms_dbfs:.2f}",
    "RMS dBFS"
)

add_kpi(
    0.55,
    f"{peak_dbfs:.2f}",
    "Peak dBFS"
)

add_kpi(
    0.75,
    f"{dominant_band}",
    "Dominant Band"
)


# ============================================================
# WAVEFORM
# ============================================================

ax1 = fig.add_axes(
    [0.07, 0.63, 0.86, 0.16]
)

ax1.set_facecolor(
    "#1F2937"
)

librosa.display.waveshow(
    audio,
    sr=sample_rate,
    ax=ax1
)

ax1.set_title(
    "FULL TRACK WAVEFORM",
    loc="left",
    color="white",
    fontsize=11,
    fontweight="bold"
)

ax1.set_xlabel(
    "Time (seconds)",
    color="#CBD5E1"
)

ax1.set_ylabel(
    "Amplitude",
    color="#CBD5E1"
)

ax1.tick_params(
    colors="#CBD5E1"
)

for spine in ax1.spines.values():

    spine.set_color(
        "#374151"
    )


# ============================================================
# FREQUENCY SPECTRUM
# ============================================================

ax2 = fig.add_axes(
    [0.07, 0.39, 0.41, 0.18]
)

ax2.set_facecolor(
    "#1F2937"
)

positive = fft_frequencies > 0

ax2.semilogx(
    fft_frequencies[positive],
    fft_magnitude[positive]
)

ax2.set_xlim(
    20,
    20000
)

ax2.set_title(
    "FREQUENCY SPECTRUM",
    loc="left",
    color="white",
    fontsize=11,
    fontweight="bold"
)

ax2.set_xlabel(
    "Frequency (Hz)",
    color="#CBD5E1"
)

ax2.set_ylabel(
    "Magnitude",
    color="#CBD5E1"
)

ax2.tick_params(
    colors="#CBD5E1"
)

ax2.grid(
    True,
    alpha=0.2
)

for spine in ax2.spines.values():

    spine.set_color(
        "#374151"
    )


# ============================================================
# BASS / MID / TREBLE
# ============================================================

ax3 = fig.add_axes(
    [0.55, 0.39, 0.38, 0.18]
)

ax3.set_facecolor(
    "#1F2937"
)

band_names = [
    "Bass",
    "Mid",
    "Treble"
]

band_values = [
    bass_percent,
    mid_percent,
    treble_percent
]

bars = ax3.barh(
    band_names,
    band_values
)

ax3.set_xlim(
    0,
    100
)

ax3.invert_yaxis()

ax3.set_title(
    "FREQUENCY BALANCE",
    loc="left",
    color="white",
    fontsize=11,
    fontweight="bold"
)

ax3.set_xlabel(
    "Relative Energy (%)",
    color="#CBD5E1"
)

ax3.tick_params(
    colors="#CBD5E1"
)

ax3.grid(
    axis="x",
    alpha=0.2
)

for bar, value in zip(
    bars,
    band_values
):

    ax3.text(
        min(value + 1, 96),
        bar.get_y()
        + bar.get_height() / 2,
        f"{value:.2f}%",
        va="center",
        color="white",
        fontsize=10,
        fontweight="bold"
    )

for spine in ax3.spines.values():

    spine.set_color(
        "#374151"
    )


# ============================================================
# SPECTROGRAM
# ============================================================

ax4 = fig.add_axes(
    [0.07, 0.10, 0.56, 0.21]
)

ax4.set_facecolor(
    "#1F2937"
)

img = librosa.display.specshow(
    spectrogram_db,
    sr=sample_rate,
    hop_length=HOP_LENGTH,
    x_axis="time",
    y_axis="hz",
    ax=ax4
)

ax4.set_ylim(
    0,
    10000
)

ax4.set_title(
    "TIME-FREQUENCY SPECTROGRAM",
    loc="left",
    color="white",
    fontsize=11,
    fontweight="bold"
)

ax4.tick_params(
    colors="#CBD5E1"
)

cbar = fig.colorbar(
    img,
    ax=ax4,
    pad=0.01
)

cbar.ax.tick_params(
    colors="#CBD5E1"
)

cbar.set_label(
    "dB",
    color="#CBD5E1"
)


# ============================================================
# FEATURE PANEL
# ============================================================

ax5 = fig.add_axes(
    [0.68, 0.10, 0.25, 0.21]
)

ax5.set_facecolor(
    "#1F2937"
)

ax5.axis(
    "off"
)


feature_text = (
    "SPECTRAL FEATURES\n"
    "────────────────────\n"
    f"Centroid     {centroid_mean:>9.2f} Hz\n"
    f"Bandwidth    {bandwidth_mean:>9.2f} Hz\n"
    f"Rolloff      {rolloff_mean:>9.2f} Hz\n"
    f"Flatness     {flatness_mean:>9.6f}\n"
    f"ZCR          {zcr_mean:>9.6f}\n\n"
    "RHYTHM\n"
    "────────────────────\n"
    f"BPM          {tempo_value:>9.2f}\n"
    f"Beats        {len(beat_times):>9d}\n\n"
    "SIGNAL\n"
    "────────────────────\n"
    f"RMS          {rms_dbfs:>9.2f} dBFS\n"
    f"Peak         {peak_dbfs:>9.2f} dBFS"
)


ax5.text(
    0.05,
    0.96,
    feature_text,
    transform=ax5.transAxes,
    fontsize=10,
    color="#E5E7EB",
    family="monospace",
    verticalalignment="top",
    linespacing=1.5
)


# ============================================================
# FOOTER
# ============================================================

fig.text(
    0.05,
    0.035,
    "Analysis: Librosa • NumPy • Matplotlib",
    fontsize=8,
    color="#64748B"
)

fig.text(
    0.93,
    0.035,
    "PROJECT 02 • STEP 14",
    fontsize=8,
    color="#64748B",
    ha="right"
)


# ============================================================
# SAVE
# ============================================================

plt.savefig(
    OUTPUT_FILE,
    dpi=160,
    bbox_inches="tight",
    facecolor=fig.get_facecolor()
)


plt.show()


# ============================================================
# RESULT
# ============================================================

print("\n" + "=" * 70)
print("STEP 14 RESULT")
print("=" * 70)

print(
    "✅ Professional waveform visualization generated."
)

print(
    "✅ Log-frequency spectrum generated."
)

print(
    "✅ Frequency balance visualization generated."
)

print(
    "✅ Spectrogram generated."
)

print(
    "✅ BPM and rhythm information integrated."
)

print(
    "✅ Spectral feature panel generated."
)

print(
    "✅ Professional dashboard generated."
)

print("\nSaved dashboard:")
print(
    f"   {OUTPUT_FILE}"
)

print("\n🎵 STEP 14 COMPLETE")