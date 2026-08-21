"""
Project-03: AI Smart Device Control & Automation Assistant
Configuration Loader
"""

import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONFIG_FILE = PROJECT_ROOT / "config" / "config.json"


def load_config():
    if not CONFIG_FILE.exists():
        raise FileNotFoundError(
            f"Configuration file not found: {CONFIG_FILE}"
        )

    with open(CONFIG_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def main():
    print("=" * 70)
    print("CONFIGURATION LOADER TEST")
    print("=" * 70)

    config = load_config()

    print("\nProject:")
    print(config["project"]["name"])

    print("\nVersion:")
    print(config["project"]["version"])

    print("\nDevices:")
    for device, settings in config["devices"].items():
        print(f"  {device}: {settings['enabled']}")

    print("\nAssistant:")
    print(f"  Response mode: {config['assistant']['response_mode']}")
    print(f"  Logging: {config['assistant']['logging_enabled']}")

    print("\n✅ Configuration loaded successfully.")


if __name__ == "__main__":
    main()