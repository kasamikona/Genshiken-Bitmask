from .Display import Display
import asyncio
from Crypto.Cipher import AES

USE_HAX = True

CHAR_CMD = "d44bc439-abfd-45a2-b575-925416129600"
CHAR_ACK = "d44bc439-abfd-45a2-b575-925416129601"
CHAR_DAT = "d44bc439-abfd-45a2-b575-92541612960a"
AES_KEY = "32672f7974ad43451d9c6c894a0e8764"

cipher = AES.new(bytes.fromhex(AES_KEY), AES.MODE_ECB)

def encrypt(packet):
	enc = cipher.encrypt(packet)
	return enc

def decrypt(packet):
	dec = cipher.decrypt(packet)
	return dec

def pad(packet):
	padlen = ((len(packet)-1)&16) + 16
	return (packet + b'\x00'*padlen)[:padlen]

def ack_handler(sender, data):
	print("Response:", decrypt(data))

class DisplayEMingLED(Display):
	@staticmethod
	def match_device(device):
		# Device 01:23:45:67:89:AB is (sometimes?) named as GLASSES-6789AB
		return device.name == ("GLASSES-" + device.address.replace(":","").upper()[-6:])

	def __init__(self):
		super().__init__()
		self.width = 36
		self.height = 12
		self.color = True
		self.bit_depth = 1
		self.max_fps = 2 if USE_HAX else 1 # Not measured
		super().generate_buffer()

	def reverse_map_bit(self, bit):
		x = bit // 12
		y = bit % 12
		if x % 2 == 1:
			y = (y + 8) % 12
		c = 0
		return (x, y, c)

	async def prepare(self, client):
		for x in range(self.width):
			for y in range(self.height):
				self.buffer[x][y] = 0
		await client.write_gatt_char(CHAR_CMD, encrypt(pad(b'\x05LEDON')), response=True) # Ensure leds on
		await self.send(client, True)
		if USE_HAX:
			# Later frames won't DATCP so do it now to set correct scroll length
			await client.write_gatt_char(CHAR_CMD, encrypt(pad(b'\x05DATCP')), response=True)
		await client.write_gatt_char(CHAR_CMD, encrypt(pad(b'\x05MODE\x01')), response=True)

	async def write_data_start(self, client, length):
		self.packet_order_index = 0
		packet = b'\x09DATS' + length.to_bytes(2,'big') + b'\x00\x00\x00'
		await client.write_gatt_char(CHAR_CMD, encrypt(pad(packet)))
		#await asyncio.sleep(0.01) # Hack because I cba to wait for DATSOK

	async def write_data_end(self, client, wait_response):
		if not USE_HAX: # else fps++
			await client.write_gatt_char(CHAR_CMD, encrypt(pad(b'\x05DATCP')))
			#await asyncio.sleep(0.01) # Hack because I cba to wait for DATCPOK
		await client.write_gatt_char(CHAR_CMD, encrypt(pad(b'\x05IMAG\x00')), response=wait_response)
		#await asyncio.sleep(0.01)

	async def write_more_data(self, client, data):
		write_amount = min(len(data), 98)
		packet = write_amount.to_bytes(1,'big') + self.packet_order_index.to_bytes(1,'big') + data[:write_amount]
		self.packet_order_index += 1
		await client.write_gatt_char(CHAR_DAT, packet)
		return write_amount

	async def wait_for_finish(self, client):
		await client.write_gatt_char(CHAR_CMD, encrypt(pad(b'\x05LEDON')), response=True) # Good enough

	async def start_notify_ack(self, client):
		await client.start_notify(CHAR_ACK, ack_handler)

	async def stop_notify_ack(self, client):
		await client.stop_notify(CHAR_ACK)
