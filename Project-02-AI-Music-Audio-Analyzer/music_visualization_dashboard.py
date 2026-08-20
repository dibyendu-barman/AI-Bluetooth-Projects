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
    "music_analysis_dashboard.png"
)


# ============================================================
# HEADER
# ============================================================

print("=" * 70)
print("AI MUSIC & AUDIO ANALYZER")
print("STEP 14 - MUSIC TRACK VISUALIZATION DASHBOARD")
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

fft_result = np.fft.rfft(
    audio
)

fft_magnitude = np.abs(
    fft_result
)

fft_frequencies = np.fft.rfftfreq(
    len(audio),
    d=1 / sample_rate
)

fft_magnitude = (
    fft_magnitude /
    len(audio)
)

dominant_index = np.argmax(
    fft_magnitude
)

dominant_frequency = (
    fft_frequencies[
        dominant_index
    ]
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


beat_times = (
    librosa.frames_to_time(
        beat_frames,
        sr=sample_rate
    )
)


# ============================================================
# DOMINANT BAND
# ============================================================

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
# CREATE DASHBOARD
# ============================================================

fig = plt.figure(
    figsize=(16, 10)
)

fig.suptitle(
    "AI Music & Audio Analyzer — Music Track Dashboard",
    fontsize=20
)


# ============================================================
# WAVEFORM
# ============================================================

ax1 = plt.subplot2grid(
    (3, 2),
    (0, 0),
    colspan=2
)


librosa.display.waveshow(
    audio,
    sr=sample_rate,
    ax=ax1
)

ax1.set_title(
    "Waveform"
)

ax1.set_xlabel(
    "Time (seconds)"
)

ax1.set_ylabel(
    "Amplitude"
)


# ============================================================
# FREQUENCY SPECTRUM
# ============================================================

ax2 = plt.subplot2grid(
    (3, 2),
    (1, 0)
)


ax2.plot(
    fft_frequencies,
    fft_magnitude
)

ax2.set_xlim(
    0,
    20000
)

ax2.set_title(
    "Frequency Spectrum"
)

ax2.set_xlabel(
    "Frequency (Hz)"
)

ax2.set_ylabel(
    "Magnitude"
)

ax2.grid(
    True,
    alpha=0.3
)


# ============================================================
# SPECTROGRAM
# ============================================================

ax3 = plt.subplot2grid(
    (3, 2),
    (1, 1)
)


img = librosa.display.specshow(
    spectrogram_db,
    sr=sample_rate,
    hop_length=HOP_LENGTH,
    x_axis="time",
    y_axis="hz",
    ax=ax3
)

ax3.set_ylim(
    0,
    10000
)

ax3.set_title(
    "Spectrogram"
)

fig.colorbar(
    img,
    ax=ax3,
    format="%+2.0f dB"
)


# ============================================================
# BASS / MID / TREBLE
# ============================================================

ax4 = plt.subplot2grid(
    (3, 2),
    (2, 0)
)


ax4.bar(
    ["Bass", "Mid", "Treble"],
    [
        bass_percent,
        mid_percent,
        treble_percent
    ]
)

ax4.set_title(
    "Bass / Mid / Treble"
)

ax4.set_ylabel(
    "Energy (%)"
)

ax4.grid(
    axis="y",
    alpha=0.3
)


# ============================================================
# INFORMATION PANEL
# ============================================================

ax5 = plt.subplot2grid(
    (3, 2),
    (2, 1)
)

ax5.axis(
    "off"
)


information = f"""
FILE INFORMATION
-------------------------
Track:
{os.path.basename(MUSIC_FILE)}

Duration:
{duration:.2f} sec

Sample Rate:
{sample_rate} Hz


SIGNAL
-------------------------
RMS:
{rms_dbfs:.2f} dBFS

Peak:
{peak_dbfs:.2f} dBFS


SPECTRAL
-------------------------
Centroid:
{centroid_mean:.2f} Hz

Bandwidth:
{bandwidth_mean:.2f} Hz

Rolloff:
{rolloff_mean:.2f} Hz

Flatness:
{flatness_mean:.6f}

ZCR:
{zcr_mean:.6f}


RHYTHM
-------------------------
BPM:
{tempo_value:.2f}

Detected Beats:
{len(beat_times)}


DOMINANT BAND
-------------------------
{dominant_band}
"""


ax5.text(
    0.02,
    0.98,
    information,
    transform=ax5.transAxes,
    fontsize=10,
    verticalalignment="top",
    family="monospace"
)


# ============================================================
# SAVE DASHBOARD
# ============================================================

plt.tight_layout(
    rect=[
        0,
        0,
        1,
        0.96
    ]
)


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
print("STEP 14 RESULT")
print("=" * 70)

print(
    "✅ Waveform visualization generated."
)

print(
    "✅ Frequency spectrum generated."
)

print(
    "✅ Spectrogram generated."
)

print(
    "✅ Bass/Mid/Treble visualization generated."
)

print(
    "✅ Audio statistics integrated."
)

print(
    "✅ BPM information integrated."
)

print(
    "✅ Music analysis dashboard generated."
)

print("\nSaved dashboard:")

print(
    f"   {OUTPUT_FILE}"
)

print("\n🎵 STEP 14 COMPLETE")