import librosa
import librosa.display
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
    "airdopes_spectrogram.png"
)


# ============================================================
# HEADER
# ============================================================

print("=" * 70)
print("AI MUSIC & AUDIO ANALYZER")
print("STEP 8 - SPECTROGRAM ANALYSIS")
print("=" * 70)


# ============================================================
# CHECK AUDIO FILE
# ============================================================

if not os.path.exists(AUDIO_FILE):

    print("\n❌ Audio file not found!")
    print(f"Expected: {AUDIO_FILE}")
    exit()


# ============================================================
# CREATE OUTPUT DIRECTORY
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
# STFT CONFIGURATION
# ============================================================

N_FFT = 2048

HOP_LENGTH = 512


print("\nSTFT Configuration")
print("-" * 70)

print(f"FFT Size    : {N_FFT}")
print(f"Hop Length  : {HOP_LENGTH}")


# ============================================================
# SHORT-TIME FOURIER TRANSFORM
# ============================================================

stft = librosa.stft(
    audio,
    n_fft=N_FFT,
    hop_length=HOP_LENGTH
)


# ============================================================
# CONVERT TO DECIBELS
# ============================================================

spectrogram_db = librosa.amplitude_to_db(
    np.abs(stft),
    ref=np.max
)


# ============================================================
# SPECTROGRAM INFORMATION
# ============================================================

frequency_bins = stft.shape[0]

time_frames = stft.shape[1]

frequency_resolution = sample_rate / N_FFT

maximum_frequency = sample_rate / 2


print("\n" + "=" * 70)
print("SPECTROGRAM INFORMATION")
print("=" * 70)

print(f"Frequency Bins      : {frequency_bins}")
print(f"Time Frames         : {time_frames}")
print(f"Frequency Resolution: {frequency_resolution:.2f} Hz")
print(f"Maximum Frequency   : {maximum_frequency:.0f} Hz")


# ============================================================
# CREATE SPECTROGRAM
# ============================================================

plt.figure(figsize=(12, 6))

librosa.display.specshow(
    spectrogram_db,
    sr=sample_rate,
    hop_length=HOP_LENGTH,
    x_axis="time",
    y_axis="hz"
)

plt.colorbar(
    format="%+2.0f dB"
)

plt.title(
    "Airdopes Joy Microphone — Spectrogram"
)

plt.xlabel("Time (seconds)")

plt.ylabel("Frequency (Hz)")

plt.ylim(0, 10000)

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
print("STEP 8 RESULT")
print("=" * 70)

print("✅ STFT calculated.")
print("✅ Spectrogram generated.")
print("✅ Time-frequency analysis completed.")
print("✅ Spectrogram graph generated.")

print(f"\n✅ Saved graph:")
print(f"   {OUTPUT_FILE}")

print("\n🎵 STEP 8 COMPLETE")