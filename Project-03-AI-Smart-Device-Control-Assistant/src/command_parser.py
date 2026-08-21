"""
Project-03: AI Smart Device Control & Automation Assistant
Step 03 - Command Parser / Intent Model
"""

# from command_model import DeviceCommand
from src.command_model import DeviceCommand


def normalize_text(text: str) -> str:
    """Normalize user command text."""
    return " ".join(text.lower().strip().split())


def parse_command(text: str) -> DeviceCommand:
    """
    Convert a simple natural-language command
    into a structured DeviceCommand.
    """

    command = normalize_text(text)

    # IoT commands
    if "turn on" in command and "light" in command:
        return DeviceCommand(
            device="iot",
            action="turn_on",
            target="desk_light"
        )

    if "turn off" in command and "light" in command:
        return DeviceCommand(
            device="iot",
            action="turn_off",
            target="desk_light"
        )

    if "turn on" in command and "fan" in command:
        return DeviceCommand(
            device="iot",
            action="turn_on",
            target="fan"
        )

    if "turn off" in command and "fan" in command:
        return DeviceCommand(
            device="iot",
            action="turn_off",
            target="fan"
        )

    # Laptop commands
    if "open" in command and "chrome" in command:
        return DeviceCommand(
            device="laptop",
            action="open",
            target="chrome"
        )

    if "open" in command and "notepad" in command:
        return DeviceCommand(
            device="laptop",
            action="open",
            target="notepad"
        )

    if "open" in command and "calculator" in command:
        return DeviceCommand(
            device="laptop",
            action="open",
            target="calculator"
        )

    if "open" in command and "vscode" in command:
        return DeviceCommand(
            device="laptop",
            action="open",
            target="vscode"
        )

    # Bluetooth commands
    if "show" in command and "bluetooth" in command:
        return DeviceCommand(
            device="bluetooth",
            action="list_devices"
        )

    # Unknown command
    return DeviceCommand(
        device="unknown",
        action="unknown",
        target=command
    )


def main():
    print("=" * 70)
    print("AI SMART DEVICE CONTROL & AUTOMATION ASSISTANT")
    print("STEP 03 - COMMAND PARSER / INTENT MODEL")
    print("=" * 70)

    test_commands = [
        "Turn on the desk light",
        "Turn off the desk light",
        "Turn on the fan",
        "Turn off the fan",
        "Open Chrome",
        "Open VSCode",
        "Show Bluetooth devices",
        "Do something unknown"
    ]

    print()

    for user_text in test_commands:
        result = parse_command(user_text)

        print(f"Input  : {user_text}")
        print(f"Device : {result.device}")
        print(f"Action : {result.action}")
        print(f"Target : {result.target}")
        print("-" * 70)

    print("✅ Command parser validation completed.")


if __name__ == "__main__":
    main()