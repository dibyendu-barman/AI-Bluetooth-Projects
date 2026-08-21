"""
Project-03: AI Smart Device Control & Automation Assistant
Step 04 - Laptop Automation Foundation
"""

import subprocess
from typing import Optional

from src.command_model import DeviceCommand


class LaptopController:
    """Controls a predefined set of safe laptop applications."""

    APPLICATIONS = {
        "notepad": ["notepad.exe"],
        "calculator": ["calc.exe"],
    }

    def open_application(self, application: str) -> bool:
        """
        Open an application from the predefined allowlist.
        """

        application = application.lower().strip()

        if application not in self.APPLICATIONS:
            print(f"❌ Application not allowed: {application}")
            return False

        try:
            subprocess.Popen(
                self.APPLICATIONS[application],
                shell=False
            )

            print(f"✅ Application launched: {application}")
            return True

        except OSError as error:
            print(f"❌ Failed to launch {application}: {error}")
            return False

    def execute(self, command: DeviceCommand) -> bool:
        """
        Execute a supported laptop DeviceCommand.
        """

        if command.device != "laptop":
            print("❌ Command is not a laptop command.")
            return False

        if command.action != "open":
            print(f"❌ Unsupported laptop action: {command.action}")
            return False

        if not command.target:
            print("❌ Laptop application target is missing.")
            return False

        return self.open_application(command.target)


def main():
    print("=" * 70)
    print("AI SMART DEVICE CONTROL & AUTOMATION ASSISTANT")
    print("STEP 04 - LAPTOP AUTOMATION FOUNDATION")
    print("=" * 70)

    controller = LaptopController()

    print("\nTesting allowed application list:")
    for application in controller.APPLICATIONS:
        print(f"  • {application}")

    print("\n✅ Laptop controller initialized.")
    print("✅ Step 04 foundation validation completed.")


if __name__ == "__main__":
    main()