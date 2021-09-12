import asyncio
from bleak import BleakScanner, BleakClient
from displays import DisplayDSD
from bleak.exc import BleakError
import System

display = None

async def get_device():
    global display
    dev = None
    display = None
    async with BleakScanner() as scanner:
        await asyncio.sleep(2) # 2 seconds should be long enough
        for d in scanner.discovered_devices:
            if check_setup_device(d):
                dev = d
                break
    return dev

def check_setup_device(device):
    global display, cipher
    if DisplayDSD.match_device(device):
        display = DisplayDSD()
        return True
    return False

async def run():
    try:
        print("Looking for compatible device")
        device = await get_device()
        if not device:
            print("No device found")
            return
        
        print("Found %s (%s), connecting" % (device.name, device.address))
        async with BleakClient(device.address) as client:
            print("Connected")
            await sendtest(client)
        print("Disconnected")
    except (BleakError, System.Exception) as err:
        print(err)
        print("\n=========================================================================\n")
        print("General Bluetooth error, is your adapter connected and enabled?")

async def sendtest(client):
    print("mtu", client.mtu_size)
    for cx in range(display.width):
        print("sendtest frame", cx)
        rsq = ((display.height-1)/2)**2
        for i in range(display.width):
            for j in range(display.height):
                dx = i - cx
                dy = j - display.height//2
                dsq = dx**2 + dy**2
                display.buffer[i][j] = 1 if dsq <= rsq else 0
        await display.send(client)


loop = asyncio.get_event_loop()
loop.run_until_complete(run())
