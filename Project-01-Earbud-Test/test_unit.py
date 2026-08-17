DEVICE_INDEX = 2
OUTPUT_DEVICE = 4
SAMPLE_RATE = 16000
DURATION = 5
CHANNELS = 1
OUTPUT_FILE = "test_recording.wav"


def test_audio_configuration():
    assert DEVICE_INDEX >= 0
    assert OUTPUT_DEVICE >= 0
    assert SAMPLE_RATE > 0
    assert DURATION > 0
    assert CHANNELS == 1


def test_output_filename():
    assert OUTPUT_FILE.endswith(".wav")