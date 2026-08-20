import librosa
import numpy as np
import os


# ============================================================
# CONFIGURATION
# ============================================================

AUDIO_FILE = os.path.join(
    "audio",
    "airdopes_test.wav"
)


# ============================================================
# HEADER
# ============================================================

print("=" * 70)
print("AI MUSIC & AUDIO ANALYZER")
print("STEP 12 - INTEGRATED AUDIO FEATURE SUMMARY")
print("=" * 70)


# ============================================================
# CHECK AUDIO FILE
# ============================================================

if not os.path.exists(AUDIO_FILE):

    print("\n❌ Audio file not found!")
    print(f"Expected: {AUDIO_FILE}")
    exit()


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


# ============================================================
# SIGNAL LEVEL ANALYSIS
# ============================================================

rms = np.sqrt(
    np.mean(audio ** 2)
)

peak = np.max(
    np.abs(audio)
)

minimum = np.min(audio)

maximum = np.max(audio)

mean_absolute = np.mean(
    np.abs(audio)
)


if rms > 0:

    rms_dbfs = 20 * np.log10(rms)

else:

    rms_dbfs = float("-inf")


if peak > 0:

    peak_dbfs = 20 * np.log10(peak)

else:

    peak_dbfs = float("-inf")


if rms > 0:

    crest_factor = peak / rms

else:

    crest_factor = 0


# ============================================================
# FFT ANALYSIS
# ============================================================

window = np.hanning(
    len(audio)
)

windowed_audio = audio * window

fft_result = np.fft.rfft(
    windowed_audio
)

magnitude = np.abs(
    fft_result
)

frequencies = np.fft.rfftfreq(
    len(audio),
    d=1 / sample_rate
)

magnitude = magnitude / len(audio)

dominant_index = np.argmax(
    magnitude
)

dominant_frequency = frequencies[
    dominant_index
]

dominant_magnitude = magnitude[
    dominant_index
]


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
    zero_crossing_rate
)


# ============================================================
# SOUND CHARACTERISTICS
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

stft_magnitude = np.abs(
    stft
)

stft_frequencies = librosa.fft_frequencies(
    sr=sample_rate,
    n_fft=N_FFT
)


bass_mask = (
    (stft_frequencies >= 20) &
    (stft_frequencies < 250)
)

mid_mask = (
    (stft_frequencies >= 250) &
    (stft_frequencies < 4000)
)

treble_mask = (
    (stft_frequencies >= 4000) &
    (stft_frequencies <= 20000)
)


bass_energy = np.mean(
    stft_magnitude[bass_mask] ** 2
)

mid_energy = np.mean(
    stft_magnitude[mid_mask] ** 2
)

treble_energy = np.mean(
    stft_magnitude[treble_mask] ** 2
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


band_percentages = {
    "Bass": bass_percent,
    "Mid": mid_percent,
    "Treble": treble_percent
}

dominant_band = max(
    band_percentages,
    key=band_percentages.get
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

beat_count = len(
    beat_times
)

onset_count = len(
    onset_times
)


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
# OVERALL SIGNAL LEVEL
# ============================================================

if peak_dbfs >= -3:

    signal_level = "Very High"

elif peak_dbfs >= -6:

    signal_level = "High"

elif peak_dbfs >= -12:

    signal_level = "Healthy"

elif peak_dbfs >= -24:

    signal_level = "Moderate"

else:

    signal_level = "Low"


# ============================================================
# PRINT INTEGRATED SUMMARY
# ============================================================

print("\n" + "=" * 70)
print("FILE INFORMATION")
print("=" * 70)

print(f"Audio File       : {AUDIO_FILE}")
print(f"Sample Rate      : {sample_rate} Hz")
print(f"Channels         : 1")
print(f"Samples          : {samples}")
print(f"Duration         : {duration:.2f} sec")


print("\n" + "=" * 70)
print("SIGNAL LEVEL")
print("=" * 70)

print(f"Minimum          : {minimum:.6f}")
print(f"Maximum          : {maximum:.6f}")
print(f"Mean Absolute    : {mean_absolute:.6f}")
print(f"RMS              : {rms:.6f}")
print(f"Peak             : {peak:.6f}")

print(f"\nRMS Level        : {rms_dbfs:.2f} dBFS")
print(f"Peak Level       : {peak_dbfs:.2f} dBFS")
print(f"Crest Factor     : {crest_factor:.3f}")
print(f"Signal Level     : {signal_level}")


print("\n" + "=" * 70)
print("FREQUENCY ANALYSIS")
print("=" * 70)

print(
    f"Dominant Frequency : "
    f"{dominant_frequency:.2f} Hz"
)

print(
    f"Dominant Magnitude : "
    f"{dominant_magnitude:.6f}"
)

print(
    f"Nyquist Frequency  : "
    f"{sample_rate / 2:.0f} Hz"
)


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

print(
    f"Brightness         : "
    f"{brightness}"
)

print(
    f"Texture            : "
    f"{texture}"
)


print("\n" + "=" * 70)
print("BASS / MID / TREBLE")
print("=" * 70)

print(
    f"Bass   (20-250 Hz)    : "
    f"{bass_percent:.2f}%"
)

print(
    f"Mid    (250-4000 Hz)  : "
    f"{mid_percent:.2f}%"
)

print(
    f"Treble (4000-20000 Hz): "
    f"{treble_percent:.2f}%"
)

print(
    f"\nDominant Band         : "
    f"{dominant_band}"
)


print("\n" + "=" * 70)
print("TEMPO / RHYTHM")
print("=" * 70)

print(
    f"Estimated BPM    : "
    f"{tempo_value:.2f}"
)

print(
    f"Detected Beats   : "
    f"{beat_count}"
)

print(
    f"Detected Onsets  : "
    f"{onset_count}"
)

print(
    f"Tempo Category   : "
    f"{tempo_category}"
)


# ============================================================
# OVERALL SUMMARY
# ============================================================

print("\n" + "=" * 70)
print("OVERALL AUDIO ANALYSIS")
print("=" * 70)

print(
    f"Signal Level     : {signal_level}"
)

print(
    f"Dominant Freq    : "
    f"{dominant_frequency:.2f} Hz"
)

print(
    f"Dominant Band    : "
    f"{dominant_band}"
)

print(
    f"Brightness       : "
    f"{brightness}"
)

print(
    f"Texture          : "
    f"{texture}"
)

print(
    f"Estimated BPM    : "
    f"{tempo_value:.2f}"
)

print(
    f"Analysis Status  : COMPLETE"
)


# ============================================================
# FINAL RESULT
# ============================================================

print("\n" + "=" * 70)
print("STEP 12 RESULT")
print("=" * 70)

print("✅ Audio information integrated.")
print("✅ Signal-level analysis integrated.")
print("✅ FFT analysis integrated.")
print("✅ Spectral features integrated.")
print("✅ Bass/Mid/Treble analysis integrated.")
print("✅ Tempo/beat analysis integrated.")
print("✅ Unified audio summary generated.")

print("\n🎵 STEP 12 COMPLETE")