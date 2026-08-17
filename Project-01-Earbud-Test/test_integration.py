import sounddevice as sd

EARBUD_NAME = "Airdopes Joy"


def get_audio_devices():
    return sd.query_devices()


def test_earbuds_detected():
    devices = get_audio_devices()

    device_names = [
        device["name"]
        for device in devices
    ]

    assert any(
        EARBUD_NAME in name
        for name in device_names
    )