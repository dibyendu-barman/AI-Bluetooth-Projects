from src.bluetooth_discovery import BluetoothDiscovery


def test_bluetooth_discovery_initialization():
    discovery = BluetoothDiscovery()

    assert discovery is not None


def test_device_record_structure():
    devices = [
        {
            "name": "Test Earbuds",
            "address": "00:11:22:33:44:55"
        }
    ]

    assert len(devices) == 1
    assert devices[0]["name"] == "Test Earbuds"
    assert devices[0]["address"] == "00:11:22:33:44:55"


def test_display_empty_device_list(capsys):
    discovery = BluetoothDiscovery()

    discovery.display_devices([])

    captured = capsys.readouterr()

    assert "No Bluetooth devices discovered" in captured.out