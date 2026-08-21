"""
Project-03
Step 04 - Laptop Controller Tests
"""

from src.command_model import DeviceCommand
from src.laptop_controller import LaptopController


def test_laptop_controller_initialization():
    controller = LaptopController()

    assert "notepad" in controller.APPLICATIONS
    assert "calculator" in controller.APPLICATIONS


def test_non_laptop_command_is_rejected():
    controller = LaptopController()

    command = DeviceCommand(
        device="iot",
        action="turn_on",
        target="desk_light"
    )

    result = controller.execute(command)

    assert result is False


def test_unsupported_application_is_rejected():
    controller = LaptopController()

    result = controller.open_application("unknown_application")

    assert result is False