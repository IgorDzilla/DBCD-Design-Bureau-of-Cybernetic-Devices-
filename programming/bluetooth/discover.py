import argparse
import asyncio

from bleak import BleakScanner

async def discover(args: argparse.Namespace):
    print("Scanning for 5 seconds, please stand by...")

    devices = await BleakScanner.discover(
        return_adv=True, cb=dict(use_bdaddr=args.macos_use_bdaddr)
    )

    for d, a in devices.values():
        print()
        print(d)
        print("-" * len(str(d)))
        print(a)


def run_discovery():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--macos-use-bdaddr",
        action="store_true",
        help="when true use Bluetooth address instead of UUID on macOS",
    )

    args = parser.parse_args()

    asyncio.run(discover(args))
