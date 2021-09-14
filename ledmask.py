import asyncio
from bleak import BleakScanner, BleakClient
from displays import DisplayDSD
from bleak.exc import BleakError
import System
import time, math

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
        print("General Bluetooth error, is your adapter connected and enabled? Is the device charged?")

async def sendtest(client):
    test_frames = 200
    sync_interval = 100
    
    start_time = time.time()
    radius = (display.height)/4
    rsq = radius**2
    for fn in range(test_frames):
        cx = (fn/3) % display.width
        cy = display.height - radius - (display.height - 2*radius) * abs(math.sin(fn/3))
        for i in range(display.width):
            for j in range(display.height):
                dx = i - cx
                dy = j - cy
                dsq = dx**2 + dy**2
                display.buffer[i][j] = 1 if dsq <= rsq else 0
        if (fn%10)==0:
            print("Generated frame", fn)
        await display.send(client, (fn%sync_interval)==0)
    await display.wait_for_finish(client)

    time_taken = time.time() - start_time
    print("Displayed %s frames in %s seconds, syncing every %s frames" % (test_frames, time_taken, sync_interval))
    print("Measured fps", test_frames / time_taken)

loop = asyncio.get_event_loop()
loop.run_until_complete(run())
