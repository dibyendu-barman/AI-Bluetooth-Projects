"""
Project-03: AI Smart Device Control & Automation Assistant
Step 05 - Bluetooth Device Discovery
"""

import asyncio
from typing import List, Dict

from bleak import BleakScanner


class BluetoothDiscovery:
    """Discover nearby Bluetooth Low Energy devices."""

    async def discover_devices(self, timeout: float = 8.0) -> List[Dict]:
        """
        Scan for nearby Bluetooth LE devices.

        Returns:
            List of dictionaries containing device name and address.
        """

        print(f"🔵 Starting Bluetooth discovery for {timeout} seconds...")

        try:
            devices = await BleakScanner.discover(timeout=timeout)

        except Exception as error:
            print(f"❌ Bluetooth discovery failed: {error}")
            return []

        discovered_devices = []

        for device in devices:
            discovered_devices.append({
                "name": device.name or "Unknown Device",
                "address": device.address
            })

        return discovered_devices

    def display_devices(self, devices: List[Dict]) -> None:
        """Display discovered Bluetooth devices."""

        if not devices:
            print("ℹ️ No Bluetooth devices discovered.")
            return

        print("\nDiscovered Bluetooth Devices:")
        print("-" * 70)

        for index, device in enumerate(devices, start=1):
            print(f"{index}. Name    : {device['name']}")
            print(f"   Address : {device['address']}")
            print("-" * 70)


async def main():
    print("=" * 70)
    print("AI SMART DEVICE CONTROL & AUTOMATION ASSISTANT")
    print("STEP 05 - BLUETOOTH DEVICE DISCOVERY")
    print("=" * 70)

    discovery = BluetoothDiscovery()

    devices = await discovery.discover_devices(timeout=8.0)

    discovery.display_devices(devices)

    print("\n✅ Bluetooth discovery operation completed.")


if __name__ == "__main__":
    asyncio.run(main())