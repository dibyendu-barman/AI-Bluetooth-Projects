import os

import sounddevice as sd
import soundfile as sf


MIC_DEVICE = 2
SAMPLE_RATE = 16000
CHANNELS = 1
DURATION = 2
TEST_FILE = "functional_test.wav"


def test_recording_workflow():
    print("\n🎤 Recording functional test...")

    audio = sd.rec(
        int(DURATION * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=CHANNELS,
        dtype="int16",
        device=MIC_DEVICE
    )

    sd.wait()

    sf.write(
        TEST_FILE,
        audio,
        SAMPLE_RATE
    )

    assert os.path.exists(TEST_FILE)

    data, rate = sf.read(TEST_FILE)

    assert rate == SAMPLE_RATE
    assert len(data) > 0

    os.remove(TEST_FILE)

    print("✅ Recording functional test passed.")