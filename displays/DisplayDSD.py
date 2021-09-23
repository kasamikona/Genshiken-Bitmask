from .Display import Display
import asyncio
from Crypto.Cipher import AES
from bleak import BleakScanner, BleakClient
from bleak.exc import BleakError

USE_HAX = True
GET_RESPONSES = False

CHAR_CMD = "d44bc439-abfd-45a2-b575-925416129600"
CHAR_ACK = "d44bc439-abfd-45a2-b575-925416129601"
CHAR_DAT = "d44bc439-abfd-45a2-b575-92541612960a"
AES_KEY = "34522A5B7A6E492C08090A9D8D2A23F8"

cipher = AES.new(bytes.fromhex(AES_KEY), AES.MODE_ECB)

def encrypt(packet):
	enc = cipher.encrypt(packet)
	return enc

def decrypt(packet):
	dec = cipher.decrypt(packet)
	return dec

def pad(packet):
	if len(packet) > 16:
		print("Packet", packet, "too long")
		return packet
	return (packet + b'\x00'*16)[:16]

def match_ble_device(device):
	# Device 01:23:45:67:89:AB is (sometimes?) named as DSD-6789AB, can change to proj_template (after pairing?)
	return device.name == ("DSD-" + device.address.replace(":","").upper()[-6:]) or device.name == "proj_template"

def ack_handler(sender, data):
	print("Response:", decrypt(data))

class DisplayDSD(Display):
	@classmethod
	async def connect(cls, addresses=None):
		if not addresses:
			addresses = []
		filter_addresses = len(addresses) > 0
		
		address = None
		async with BleakScanner() as scanner:
			await asyncio.sleep(2) # 2 seconds should be long enough
			for d in scanner.discovered_devices:
				if filter_addresses and d.address not in addresses:
					break
				if match_ble_device(d):
					print("Found %s (%s)" % (d.name, d.address, ))
					address = d.address
					break

		if not address:
			return None

		try:
			client = BleakClient(address)
			if not await client.connect():
				return None

			disp = cls(client)
			client.set_disconnected_callback(disp._disconnect_unexpected)
			if GET_RESPONSES:
				await disp.start_notify_ack(client)
			await disp.prepare()

			print("Connected to %s" % (address))
			return disp
		except BleakError:
			return None

	async def disconnect(self):
		if not self.is_connected:
			return

		if GET_RESPONSES:
			await display.stop_notify_ack(self.client)
		await self.client.disconnect()

		self.is_connected = False
		print("Disconnected")

	def _disconnect_unexpected(self, cbclient=None):
		if self.is_connected:
			self.is_connected = False
			print("Disconnected unexpectedly")

	def __init__(self, client=None):
		super().__init__()
		self.width = 48
		self.height = 12
		self.color = False
		self.bit_depth = 1
		self.max_fps = 10 if USE_HAX else 7.5 # Measured up to 10.5 fps with hax, 8.0 without
		super().generate_buffer()
		self.client = client
		self.is_connected = True

	def reverse_map_bit(self, bit):
		x = bit // 12
		y = bit % 12
		if x % 2 == 1:
			y = (y + 8) % 12
		c = 0
		return (x, y, c)

	async def prepare(self):
		try:
			for x in range(self.width):
				for y in range(self.height):
					self.buffer[x][y] = 0

			await self.client.write_gatt_char(CHAR_CMD, encrypt(pad(b'\x05LEDON')), response=True) # Ensure leds on
			await self.send(True)

			if USE_HAX:
				# Later frames won't DATCP so do it now to set correct scroll length
				await self.client.write_gatt_char(CHAR_CMD, encrypt(pad(b'\x05DATCP')), response=True)

			await self.client.write_gatt_char(CHAR_CMD, encrypt(pad(b'\x05MODE\x01')), response=True)
		except BleakError:
			self._disconnect_unexpected()

	async def send(self, wait_response=False):
		try:
			await super().send(wait_response)
		except BleakError:
			self._disconnect_unexpected()

	async def write_data_start(self, length):
		try:
			packet = b'\x08DATS' + length.to_bytes(2,'big') + b'\x00\x00'
			await self.client.write_gatt_char(CHAR_CMD, encrypt(pad(packet)))
			#await asyncio.sleep(0.01) # Hack because I cba to wait for DATSOK
		except BleakError:
			self._disconnect_unexpected()

	async def write_data_end(self, wait_response):
		try:
			if not USE_HAX:
				await self.client.write_gatt_char(CHAR_CMD, encrypt(pad(b'\x05DATCP')))
				#await asyncio.sleep(0.01) # Hack because I cba to wait for DATCPOK
			await self.client.write_gatt_char(CHAR_CMD, encrypt(pad(b'\x05MODE\x01')), response=wait_response)
			#await asyncio.sleep(0.01)
		except BleakError:
			self._disconnect_unexpected()

	async def write_more_data(self, data):
		write_amount = min(len(data), 15)
		try:
			packet = write_amount.to_bytes(1,'big') + data[:write_amount]
			await self.client.write_gatt_char(CHAR_DAT, encrypt(pad(packet)))
		except BleakError:
			self._disconnect_unexpected()
		return write_amount

	async def wait_for_finish(self):
		try:
			await self.client.write_gatt_char(CHAR_CMD, encrypt(pad(b'\x05LEDON')), response=True) # Good enough
		except BleakError:
			self._disconnect_unexpected()

	async def start_notify_ack(self):
		try:
			await self.client.start_notify(CHAR_ACK, ack_handler)
		except BleakError:
			self._disconnect_unexpected()

	async def stop_notify_ack(self):
		try:
			await self.client.stop_notify(CHAR_ACK)
		except BleakError:
			self._disconnect_unexpected()
