import librosa
import numpy as np
import os

# ============================================================
# CONFIGURATION
# ============================================================

AUDIO_FILE = os.path.join("audio", "airdopes_test.wav")


# ============================================================
# HEADER
# ============================================================

print("=" * 70)
print("AI MUSIC & AUDIO ANALYZER")
print("STEP 4 - WAV AUDIO ANALYSIS")
print("=" * 70)


# ============================================================
# CHECK FILE
# ============================================================

if not os.path.exists(AUDIO_FILE):
    print("\n❌ Audio file not found!")
    print(f"Expected file: {AUDIO_FILE}")
    exit()


print(f"\nAudio File: {AUDIO_FILE}")


# ============================================================
# LOAD AUDIO
# ============================================================

try:

    audio, sample_rate = librosa.load(
        AUDIO_FILE,
        sr=None,
        mono=False
    )

    print("\n✅ Audio loaded successfully.")

except Exception as error:

    print("\n❌ Failed to load audio.")
    print(f"Error: {error}")
    exit()


# ============================================================
# AUDIO INFORMATION
# ============================================================

print("\n" + "=" * 70)
print("AUDIO INFORMATION")
print("=" * 70)

print(f"Sample Rate : {sample_rate} Hz")

if audio.ndim == 1:

    channels = 1
    samples = len(audio)

else:

    channels = audio.shape[0]
    samples = audio.shape[1]


duration = samples / sample_rate

print(f"Channels    : {channels}")
print(f"Samples     : {samples}")
print(f"Duration    : {duration:.2f} seconds")


# ============================================================
# BASIC SIGNAL ANALYSIS
# ============================================================

if audio.ndim > 1:

    analysis_audio = np.mean(audio, axis=0)

else:

    analysis_audio = audio


rms = np.sqrt(np.mean(analysis_audio ** 2))
peak = np.max(np.abs(analysis_audio))


print("\n" + "=" * 70)
print("SIGNAL ANALYSIS")
print("=" * 70)

print(f"RMS Amplitude : {rms:.6f}")
print(f"Peak Amplitude: {peak:.6f}")


# ============================================================
# dBFS CALCULATION
# ============================================================

if rms > 0:

    rms_dbfs = 20 * np.log10(rms)

else:

    rms_dbfs = float("-inf")


if peak > 0:

    peak_dbfs = 20 * np.log10(peak)

else:

    peak_dbfs = float("-inf")


print(f"RMS Level     : {rms_dbfs:.2f} dBFS")
print(f"Peak Level    : {peak_dbfs:.2f} dBFS")


# ============================================================
# FINAL RESULT
# ============================================================

print("\n" + "=" * 70)
print("STEP 4 RESULT")
print("=" * 70)

print("✅ WAV file successfully loaded.")
print("✅ Audio information extracted.")
print("✅ RMS level calculated.")
print("✅ Peak level calculated.")
print("✅ dBFS levels calculated.")

print("\n🎵 STEP 4 COMPLETE")