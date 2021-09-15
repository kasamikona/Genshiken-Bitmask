import asyncio
from bleak import BleakScanner, BleakClient
from bleak.exc import BleakError
import displays

GET_RESPOSNES = False
SCAN_SECONDS = 2 # 2 seconds should be long enough
AUTO_SCAN_CLASSES = [ # Update as new displays are added
    displays.DisplayDSD
]

client = None
display = None

async def get_device(displayClasses=None):
    bt_device = None
    display = None

    async with BleakScanner() as scanner:
        await asyncio.sleep(SCAN_SECONDS) 
        for d in scanner.discovered_devices:
            display = check_setup_display(d, displayClasses)
            if display:
                bt_device = d
                break

    return (bt_device, display)

def check_setup_display(bt_device, displayClasses=None):
    if not displayClasses:
        displayClasses = AUTO_SCAN_CLASSES

    for displayClass in displayClasses:
        if displayClass.match_device(bt_device):
            return displayClass()

    return None

async def connect(displayClasses=None):
    global client, display
    if client:
        print("Already connected")
        return False
    
    error_suffix = "Is the BLE adapter connected and enabled? Is the display charged and switched on?"
    try:
        print("Looking for compatible display")
        bt_device, display = await get_device(displayClasses)

        if not display:
            print("No display found.", error_suffix)
            return False

        print("Found %s (%s), using display class %s..." % (bt_device.name, bt_device.address, type(display).__name__))
        client = BleakClient(bt_device.address)
        await client.connect()

        if GET_RESPOSNES:
            await display.start_notify_ack(client)

        print("Connected")
        return True

    except (BleakError, System.Exception) as err:
        print(err)
        print("\nConnection error.", error_suffix)
        return False

async def disconnect():
    global client, display

    if not client:
        return

    if GET_RESPOSNES:
        await display.stop_notify_ack(client)

    await client.disconnect()
    client = None
    display = None
    print("Disconnected")
