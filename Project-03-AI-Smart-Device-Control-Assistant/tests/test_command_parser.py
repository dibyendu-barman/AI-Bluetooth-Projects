"""
Project-03
Step 03 - Command Parser Tests
"""

from src.command_parser import parse_command


def test_turn_on_light():
    command = parse_command("Turn on the desk light")

    assert command.device == "iot"
    assert command.action == "turn_on"
    assert command.target == "desk_light"


def test_turn_off_fan():
    command = parse_command("Turn off the fan")

    assert command.device == "iot"
    assert command.action == "turn_off"
    assert command.target == "fan"


def test_open_chrome():
    command = parse_command("Open Chrome")

    assert command.device == "laptop"
    assert command.action == "open"
    assert command.target == "chrome"


def test_bluetooth_devices():
    command = parse_command("Show Bluetooth devices")

    assert command.device == "bluetooth"
    assert command.action == "list_devices"


def test_unknown_command():
    command = parse_command("Play something random")

    assert command.device == "unknown"
    assert command.action == "unknown"