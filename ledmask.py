import asyncio
from bleak import BleakScanner, BleakClient
from Crypto.Cipher import AES
from displays import DSD

cipher = None
display = None

def encrypt(packet):
    enc = cipher.encrypt(bytes.fromhex(packet)).hex()
    print("Encrypted %s to %s" % (packet, enc))
    return enc

def decrypt(packet):
    dec = cipher.decrypt(bytes.fromhex(packet)).hex()
    print("Decrypted %s to %s" % (packet, dec))
    return dec

async def get_device():
    global display, cipher
    devices = await BleakScanner.discover()
    dev = None
    display = None
    cipher = None
    for d in devices:
        if check_setup_device(d):
            dev = d
            break
    return dev

def check_setup_device(device):
    global display, cipher
    if DSD.match_device(device):
        display = DSD()
    
    if not display:
        return False
    cipher = AES.new(bytes.fromhex(display.aes_key), AES.MODE_ECB)
    return True

async def run():
    device = await get_device()
    if not device:
        print("No device found")
        return
    
    print("Found %s (%s), connecting" % (device.name, device.address))
    async with BleakClient(device.address) as client:
        print("Connected, begin main program")
        await sendtest(client)
        print("Done")
    print("Disconnected")

async def sendtest(client):
    await client.write_gatt_char(display.char_cmd, bytearray.fromhex(encrypt("0844 4154 5300 4800 0000 0000 0000 0000"))) # DATS
    await asyncio.sleep(0.5) # Hack because I cba to wait for DATSOK
    await client.write_gatt_char(display.char_dat, bytearray.fromhex(encrypt("0fff ffff ffff ffff ffff ffff ff00 0000"))) # data
    await client.write_gatt_char(display.char_dat, bytearray.fromhex(encrypt("0fff ffff ffff ffff ffff ffff ff00 0000"))) # data
    await client.write_gatt_char(display.char_dat, bytearray.fromhex(encrypt("0fff ffff ffff ffff ffff ffff ff00 0000"))) # data
    await client.write_gatt_char(display.char_dat, bytearray.fromhex(encrypt("0fff ffff ffff ffff ffff ffff ff00 0000"))) # data
    await client.write_gatt_char(display.char_dat, bytearray.fromhex(encrypt("0cff ffff ffff ffff ffff ffff ff00 0000"))) # data
    await client.write_gatt_char(display.char_cmd, bytearray.fromhex(encrypt("0544 4154 4350 0000 0000 0000 0000 0000"))) # DATCP
    await asyncio.sleep(0.5) # Hack because I cba to wait for DATCPOK
    await client.write_gatt_char(display.char_cmd, bytearray.fromhex(encrypt("054d 4f44 4501 0000 0000 0000 0000 0000"))) # MODE
    await asyncio.sleep(0.5) # Hack because idk when to end

loop = asyncio.get_event_loop()
loop.run_until_complete(run())
