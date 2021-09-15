from .DisplayBase import DisplayBase
import asyncio
from Crypto.Cipher import AES

USE_HAX = False

CHAR_CMD = "d44bc439-abfd-45a2-b575-925416129600"
CHAR_ACK = "d44bc439-abfd-45a2-b575-925416129601"
CHAR_DAT = "d44bc439-abfd-45a2-b575-92541612960a"
AES_KEY = "34522A5B7A6E492C08090A9D8D2A23F8"

cipher = AES.new(bytes.fromhex(AES_KEY), AES.MODE_ECB)

def encrypt(packet):
    enc = cipher.encrypt(packet)
    #print("Encrypted %s to %s" % (packet.hex(), enc.hex()))
    return enc

def decrypt(packet):
    dec = cipher.decrypt(packet)
    #print("Decrypted %s to %s" % (packet.hex(), dec.hex()))
    return dec

def pad(packet):
    padlen = ((len(packet)-1)&16) + 16
    return (packet + b'\x00'*padlen)[:padlen]

def ack_handler(sender, data):
    print("Response:", decrypt(data))

class DisplayDSD(DisplayBase):
    @staticmethod
    def match_device(device):
        # Device 01:23:45:67:89:AB is (sometimes?) named as DSD-6789AB, can change to proj_template (after pairing?)
        return device.name == ("DSD-" + device.address.replace(":","").upper()[-6:]) or device.name == "proj_template"

    def __init__(self):
        self.width = 48
        self.height = 12
        self.color = False
        self.bit_depth = 1
        self.max_fps = 10 if USE_HAX else 7.5 # Measured up to 10.5 fps with hax, 8.0 without
        super().generate_buffer()

    def reverse_map_bit(self, bit):
        x = bit // 12
        y = bit % 12
        if x % 2 == 1:
            y = (y + 8) % 12
        c = 0
        return (x, y, c)

    async def write_data_start(self, client, length):
        packet = b'\x08DATS'
        if USE_HAX: # fps++
            packet += b'\x00\x00' 
        else:
            packet += length.to_bytes(2,'big')
        packet += b'\x00\x00'
        await client.write_gatt_char(CHAR_CMD, encrypt(pad(packet)))
        await asyncio.sleep(0.01) # Hack because I cba to wait for DATSOK

    async def write_data_end(self, client, wait_response):
        if not USE_HAX: # else fps++
            await client.write_gatt_char(CHAR_CMD, encrypt(pad(b'\x05DATCP')))
            await asyncio.sleep(0.01) # Hack because I cba to wait for DATCPOK
        await client.write_gatt_char(CHAR_CMD, encrypt(pad(b'\x05MODE\x01')), response=wait_response)
        await asyncio.sleep(0.01)

    async def write_more_data(self, client, data):
        write_amount = min(len(data), 15)
        packet = write_amount.to_bytes(1,'big')
        packet += data[:write_amount]
        await client.write_gatt_char(CHAR_DAT, encrypt(pad(packet)))
        return write_amount

    async def wait_for_finish(self, client):
        await client.write_gatt_char(CHAR_CMD, encrypt(pad(b'\x05LEDON')), response=True) # Good enough

    async def start_notify_ack(self, client):
        await client.start_notify(CHAR_ACK, ack_handler)

    async def stop_notify_ack(self, client):
        await client.stop_notify(CHAR_ACK)
