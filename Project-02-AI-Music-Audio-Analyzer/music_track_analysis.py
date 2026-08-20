import librosa
import numpy as np
import os


# ============================================================
# CONFIGURATION
# ============================================================

MUSIC_DIR = "music"

SUPPORTED_EXTENSIONS = [
    ".wav",
    ".mp3",
    ".flac",
    ".ogg",
    ".m4a"
]


# ============================================================
# HEADER
# ============================================================

print("=" * 70)
print("AI MUSIC & AUDIO ANALYZER")
print("STEP 13 - REAL MUSIC FILE INPUT & MUSIC TRACK ANALYSIS")
print("=" * 70)


# ============================================================
# CHECK MUSIC DIRECTORY
# ============================================================

if not os.path.exists(MUSIC_DIR):

    print("\n❌ Music folder not found!")
    print(f"Expected folder: {MUSIC_DIR}")
    exit()


# ============================================================
# FIND MUSIC FILES
# ============================================================

music_files = []

for filename in os.listdir(MUSIC_DIR):

    extension = os.path.splitext(
        filename
    )[1].lower()

    if extension in SUPPORTED_EXTENSIONS:

        music_files.append(filename)


# ============================================================
# CHECK FILES
# ============================================================

if not music_files:

    print("\n❌ No supported music file found.")

    print("\nSupported formats:")

    for extension in SUPPORTED_EXTENSIONS:

        print(f"   {extension}")

    print("\nPlace a music file inside:")
    print("   music\\")

    exit()


# ============================================================
# DISPLAY AVAILABLE FILES
# ============================================================

print("\nAvailable Music Files")
print("-" * 70)

for index, filename in enumerate(
    music_files,
    start=1
):

    print(
        f"[{index}] {filename}"
    )


# ============================================================
# SELECT FIRST FILE
# ============================================================

selected_file = music_files[0]

music_file = os.path.join(
    MUSIC_DIR,
    selected_file
)


print("\nSelected Music File")
print("-" * 70)

print(
    f"File : {selected_file}"
)


# ============================================================
# LOAD MUSIC
# ============================================================

try:

    audio, sample_rate = librosa.load(
        music_file,
        sr=None,
        mono=True
    )

    print("\n✅ Music file loaded successfully.")

except Exception as error:

    print("\n❌ Failed to load music file.")

    print(
        f"Error: {error}"
    )

    exit()


# ============================================================
# BASIC INFORMATION
# ============================================================

samples = len(audio)

duration = samples / sample_rate

channels = 1


print("\n" + "=" * 70)
print("MUSIC FILE INFORMATION")
print("=" * 70)

print(
    f"File Name   : {selected_file}"
)

print(
    f"Sample Rate : {sample_rate} Hz"
)

print(
    f"Channels    : {channels}"
)

print(
    f"Samples     : {samples}"
)

print(
    f"Duration    : {duration:.2f} sec"
)


# ============================================================
# SIGNAL LEVEL
# ============================================================

rms = np.sqrt(
    np.mean(audio ** 2)
)

peak = np.max(
    np.abs(audio)
)


if rms > 0:

    rms_dbfs = 20 * np.log10(
        rms
    )

else:

    rms_dbfs = float("-inf")


if peak > 0:

    peak_dbfs = 20 * np.log10(
        peak
    )

else:

    peak_dbfs = float("-inf")


print("\n" + "=" * 70)
print("SIGNAL LEVEL")
print("=" * 70)

print(
    f"RMS Amplitude : "
    f"{rms:.6f}"
)

print(
    f"Peak Amplitude: "
    f"{peak:.6f}"
)

print(
    f"RMS Level     : "
    f"{rms_dbfs:.2f} dBFS"
)

print(
    f"Peak Level    : "
    f"{peak_dbfs:.2f} dBFS"
)


# ============================================================
# SPECTRAL CENTROID
# ============================================================

spectral_centroid = librosa.feature.spectral_centroid(
    y=audio,
    sr=sample_rate
)[0]


centroid_mean = np.mean(
    spectral_centroid
)


# ============================================================
# SPECTRAL BANDWIDTH
# ============================================================

spectral_bandwidth = librosa.feature.spectral_bandwidth(
    y=audio,
    sr=sample_rate
)[0]


bandwidth_mean = np.mean(
    spectral_bandwidth
)


# ============================================================
# SPECTRAL ROLLOFF
# ============================================================

spectral_rolloff = librosa.feature.spectral_rolloff(
    y=audio,
    sr=sample_rate,
    roll_percent=0.85
)[0]


rolloff_mean = np.mean(
    spectral_rolloff
)


# ============================================================
# SPECTRAL FLATNESS
# ============================================================

spectral_flatness = librosa.feature.spectral_flatness(
    y=audio
)[0]


flatness_mean = np.mean(
    spectral_flatness
)


# ============================================================
# ZERO CROSSING RATE
# ============================================================

zero_crossing_rate = librosa.feature.zero_crossing_rate(
    audio
)[0]


zcr_mean = np.mean(
    zero_crossing_rate
)


# ============================================================
# PRINT SPECTRAL FEATURES
# ============================================================

print("\n" + "=" * 70)
print("SPECTRAL FEATURES")
print("=" * 70)

print(
    f"Spectral Centroid  : "
    f"{centroid_mean:.2f} Hz"
)

print(
    f"Spectral Bandwidth : "
    f"{bandwidth_mean:.2f} Hz"
)

print(
    f"Spectral Rolloff   : "
    f"{rolloff_mean:.2f} Hz"
)

print(
    f"Spectral Flatness  : "
    f"{flatness_mean:.6f}"
)

print(
    f"Zero Crossing Rate : "
    f"{zcr_mean:.6f}"
)


# ============================================================
# BASS / MID / TREBLE
# ============================================================

N_FFT = 2048

HOP_LENGTH = 512


stft = librosa.stft(
    audio,
    n_fft=N_FFT,
    hop_length=HOP_LENGTH
)


magnitude = np.abs(
    stft
)


frequencies = librosa.fft_frequencies(
    sr=sample_rate,
    n_fft=N_FFT
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
# PRINT FREQUENCY BANDS
# ============================================================

print("\n" + "=" * 70)
print("BASS / MID / TREBLE")
print("=" * 70)

print(
    f"Bass   : {bass_percent:.2f}%"
)

print(
    f"Mid    : {mid_percent:.2f}%"
)

print(
    f"Treble : {treble_percent:.2f}%"
)

print(
    f"Dominant Band : {dominant_band}"
)


# ============================================================
# TEMPO / BEAT ANALYSIS
# ============================================================

onset_envelope = librosa.onset.onset_strength(
    y=audio,
    sr=sample_rate
)


tempo, beat_frames = librosa.beat.beat_track(
    onset_envelope=onset_envelope,
    sr=sample_rate
)


tempo_value = float(
    np.asarray(tempo).flatten()[0]
)


beat_times = librosa.frames_to_time(
    beat_frames,
    sr=sample_rate
)


onset_frames = librosa.onset.onset_detect(
    onset_envelope=onset_envelope,
    sr=sample_rate
)


onset_times = librosa.frames_to_time(
    onset_frames,
    sr=sample_rate
)


# ============================================================
# TEMPO CATEGORY
# ============================================================

if tempo_value < 60:

    tempo_category = "Very Slow"

elif tempo_value < 90:

    tempo_category = "Slow"

elif tempo_value < 120:

    tempo_category = "Moderate"

elif tempo_value < 160:

    tempo_category = "Fast"

else:

    tempo_category = "Very Fast"


# ============================================================
# PRINT TEMPO
# ============================================================

print("\n" + "=" * 70)
print("TEMPO / RHYTHM")
print("=" * 70)

print(
    f"Estimated BPM : "
    f"{tempo_value:.2f}"
)

print(
    f"Detected Beats: "
    f"{len(beat_times)}"
)

print(
    f"Detected Onsets: "
    f"{len(onset_times)}"
)

print(
    f"Tempo Category : "
    f"{tempo_category}"
)


# ============================================================
# FINAL MUSIC ANALYSIS
# ============================================================

print("\n" + "=" * 70)
print("MUSIC TRACK ANALYSIS SUMMARY")
print("=" * 70)

print(
    f"Track          : "
    f"{selected_file}"
)

print(
    f"Duration       : "
    f"{duration:.2f} sec"
)

print(
    f"BPM            : "
    f"{tempo_value:.2f}"
)

print(
    f"Dominant Band  : "
    f"{dominant_band}"
)

print(
    f"Centroid       : "
    f"{centroid_mean:.2f} Hz"
)

print(
    f"RMS Level      : "
    f"{rms_dbfs:.2f} dBFS"
)

print(
    f"Peak Level     : "
    f"{peak_dbfs:.2f} dBFS"
)


# ============================================================
# FINAL RESULT
# ============================================================

print("\n" + "=" * 70)
print("STEP 13 RESULT")
print("=" * 70)

print(
    "✅ Real music file detected."
)

print(
    "✅ Music file loaded."
)

print(
    "✅ Audio information extracted."
)

print(
    "✅ Signal level analyzed."
)

print(
    "✅ Spectral features calculated."
)

print(
    "✅ Bass/Mid/Treble calculated."
)

print(
    "✅ Tempo estimated."
)

print(
    "✅ Beat detection completed."
)

print(
    "✅ Music track analysis completed."
)

print("\n🎵 STEP 13 COMPLETE")