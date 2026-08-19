import sounddevice as sd

print("=" * 70)
print("AI MUSIC & AUDIO ANALYZER")
print("AUDIO DEVICE DETECTION")
print("=" * 70)

print("\nAvailable Audio Devices:\n")

devices = sd.query_devices()

for index, device in enumerate(devices):
    print(f"[{index}] {device['name']}")
    print(f"     Input Channels : {device['max_input_channels']}")
    print(f"     Output Channels: {device['max_output_channels']}")
    print(f"     Sample Rate    : {device['default_samplerate']}")
    print("-" * 70)