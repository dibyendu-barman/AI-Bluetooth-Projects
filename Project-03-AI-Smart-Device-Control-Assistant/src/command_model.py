"""
Project-03: AI Smart Device Control & Automation Assistant
Step 02 - Device Command Model
"""

from dataclasses import dataclass, asdict
from typing import Optional
import json


@dataclass
class DeviceCommand:
    device: str
    action: str
    target: Optional[str] = None
    value: Optional[str] = None

    def to_dict(self):
        return asdict(self)

    def to_json(self):
        return json.dumps(self.to_dict(), indent=4)


def main():
    print("=" * 70)
    print("AI SMART DEVICE CONTROL & AUTOMATION ASSISTANT")
    print("STEP 02 - DEVICE COMMAND MODEL")
    print("=" * 70)

    command = DeviceCommand(
        device="iot",
        action="turn_on",
        target="desk_light"
    )

    print("\nGenerated Command:")
    print(command.to_json())

    print("\n✅ Command model created successfully.")
    print("✅ Step 02 basic validation completed.")


if __name__ == "__main__":
    main()