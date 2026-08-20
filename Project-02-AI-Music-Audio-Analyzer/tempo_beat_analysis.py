import librosa
import librosa.display
import numpy as np
import matplotlib.pyplot as plt
import os


# ============================================================
# CONFIGURATION
# ============================================================

AUDIO_FILE = os.path.join(
    "audio",
    "airdopes_test.wav"
)

OUTPUT_DIR = "reports"

OUTPUT_FILE = os.path.join(
    OUTPUT_DIR,
    "airdopes_tempo_beats.png"
)


# ============================================================
# HEADER
# ============================================================

print("=" * 70)
print("AI MUSIC & AUDIO ANALYZER")
print("STEP 11 - TEMPO / BPM & BEAT ANALYSIS")
print("=" * 70)


# ============================================================
# CHECK AUDIO FILE
# ============================================================

if not os.path.exists(AUDIO_FILE):

    print("\n❌ Audio file not found!")
    print(f"Expected: {AUDIO_FILE}")
    exit()


# ============================================================
# CREATE REPORT DIRECTORY
# ============================================================

os.makedirs(
    OUTPUT_DIR,
    exist_ok=True
)


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
# AUDIO INFORMATION
# ============================================================

samples = len(audio)

duration = samples / sample_rate

print("\nAudio Information")
print("-" * 70)

print(f"Sample Rate : {sample_rate} Hz")
print(f"Samples     : {samples}")
print(f"Duration    : {duration:.2f} seconds")


# ============================================================
# ONSET STRENGTH
# ============================================================

onset_envelope = librosa.onset.onset_strength(
    y=audio,
    sr=sample_rate
)


# ============================================================
# TEMPO ESTIMATION
# ============================================================

tempo, beat_frames = librosa.beat.beat_track(
    onset_envelope=onset_envelope,
    sr=sample_rate
)


# ============================================================
# HANDLE LIBROSA TEMPO OUTPUT
# ============================================================

tempo_value = float(
    np.asarray(tempo).flatten()[0]
)


# ============================================================
# BEAT TIMES
# ============================================================

beat_times = librosa.frames_to_time(
    beat_frames,
    sr=sample_rate
)


# ============================================================
# ONSET TIMES
# ============================================================

onset_frames = librosa.onset.onset_detect(
    onset_envelope=onset_envelope,
    sr=sample_rate
)

onset_times = librosa.frames_to_time(
    onset_frames,
    sr=sample_rate
)


# ============================================================
# BEAT COUNT
# ============================================================

beat_count = len(beat_times)

onset_count = len(onset_times)


# ============================================================
# AVERAGE ONSET STRENGTH
# ============================================================

if len(onset_envelope) > 0:

    average_onset_strength = np.mean(
        onset_envelope
    )

    maximum_onset_strength = np.max(
        onset_envelope
    )

else:

    average_onset_strength = 0

    maximum_onset_strength = 0


# ============================================================
# PRINT RESULTS
# ============================================================

print("\n" + "=" * 70)
print("TEMPO / BEAT RESULTS")
print("=" * 70)

print(
    f"Estimated Tempo : "
    f"{tempo_value:.2f} BPM"
)

print(
    f"Detected Beats  : "
    f"{beat_count}"
)

print(
    f"Detected Onsets : "
    f"{onset_count}"
)

print(
    f"Average Onset Strength : "
    f"{average_onset_strength:.6f}"
)

print(
    f"Maximum Onset Strength : "
    f"{maximum_onset_strength:.6f}"
)


# ============================================================
# PRINT BEAT TIMELINE
# ============================================================

print("\nBeat Timeline")
print("-" * 70)

if beat_count == 0:

    print("No beats detected.")

else:

    for index, beat_time in enumerate(
        beat_times,
        start=1
    ):

        print(
            f"Beat {index:02d} : "
            f"{beat_time:.3f} sec"
        )


# ============================================================
# TEMPO INTERPRETATION
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


print("\n" + "=" * 70)
print("TEMPO CATEGORY")
print("=" * 70)

print(
    f"Category : {tempo_category}"
)


# ============================================================
# CREATE BEAT VISUALIZATION
# ============================================================

times = librosa.times_like(
    onset_envelope,
    sr=sample_rate
)


plt.figure(
    figsize=(12, 5)
)

plt.plot(
    times,
    onset_envelope,
    label="Onset Strength"
)

if beat_count > 0:

    plt.vlines(
        beat_times,
        0,
        np.max(onset_envelope),
        alpha=0.6,
        linestyle="--",
        label="Detected Beats"
    )


plt.title(
    "Airdopes Joy — Tempo and Beat Analysis"
)

plt.xlabel(
    "Time (seconds)"
)

plt.ylabel(
    "Onset Strength"
)

plt.xlim(
    0,
    duration
)

plt.grid(
    True,
    alpha=0.3
)

plt.legend()

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
print("STEP 11 RESULT")
print("=" * 70)

print(
    "✅ Onset strength calculated."
)

print(
    "✅ Tempo estimated."
)

print(
    "✅ Beat tracking completed."
)

print(
    "✅ Beat timeline generated."
)

print(
    "✅ Tempo/beat visualization generated."
)

print("\nSaved graph:")

print(
    f"   {OUTPUT_FILE}"
)

print("\n🎵 STEP 11 COMPLETE")