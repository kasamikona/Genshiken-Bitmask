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

def reverse_map_bit(bit):
	x = bit // 12
	y = bit % 12
	if x % 2 == 1:
		y = (y + 8) % 12
	c = 0
	return (x, y, c)

class DisplayDSD(Display):
	def __init__(self, client=None):
		super().__init__()
		self.client = client
		self.width = 48
		self.height = 12
		self.color = False
		self.bit_depth = 1
		self.buffer = self.buffer = [[0]*self.height for x in range(self.width)]
		self.max_fps = 10 if USE_HAX else 7.5 # Measured up to 10.5 fps with hax, 8.0 without
		self.is_connected = True
		self.num_bits = self.width * self.height * self.bit_depth
		# Reverse map output bits into pixel buffer
		self.bit_remap = [0]*self.num_bits
		for i in range(self.num_bits):
			self.bit_remap[i] = reverse_map_bit(i) 

	@classmethod
	async def connect(cls, addresses=None, dispargs=None):
		if not addresses:
			addresses = []
		filter_addresses = len(addresses) > 0
		
		address = None
		try:
			async with BleakScanner() as scanner:
				await asyncio.sleep(2) # 2 seconds should be long enough
				for d in scanner.discovered_devices:
					if filter_addresses and d.address not in addresses:
						break
					if match_ble_device(d):
						print("DisplayDSD found %s (%s)" % (d.name, d.address))
						address = d.address
						break
		except OSError:
			pass
		
		if not address:
			return None
			
		#address = "00:2A:EC:00:A0:D6"

		#await asyncio.sleep(2) # Time for connection to reset after scanning

		try:
			client = BleakClient(address)
			if not await client.connect():
				#await client.disconnect()
				return None

			disp = cls(client)
			client.set_disconnected_callback(disp._disconnect_unexpected)
			if GET_RESPONSES:
				await disp.start_notify_ack(client)
			await disp.prepare()

			print("Connected to %s" % (address))
			return disp
		except BleakError as e:
			print(e)
			return None

	async def disconnect(self):
		if not self.is_connected:
			return
		self.is_connected = False

		if GET_RESPONSES:
			await display.stop_notify_ack(self.client)
		await self.client.disconnect()

		print("Disconnected")

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
			await asyncio.sleep(1) # Let it stabilize and stop flashing
		except BleakError as e:
			print(e)
			await self.client.disconnect()

	async def send(self, wait_response=False):
		try:
			out_bytes = self._get_output_bytes()
			await self._write_data_start(len(out_bytes))
			while len(out_bytes) > 0:
				num_written_bytes = await self._write_more_data(out_bytes)
				out_bytes = out_bytes[num_written_bytes:]
			await self._write_data_end(wait_response)
		except BleakError as e:
			print(e)
			await self.client.disconnect()

	async def wait_for_finish(self):
		try:
			await self.client.write_gatt_char(CHAR_CMD, encrypt(pad(b'\x05LEDON')), response=True) # Good enough
		except BleakError as e:
			print(e)
			await self.client.disconnect()

	def _get_output_bytes(self):
		num_bytes = (self.num_bits + 7) // 8
		out_bytes = bytearray(num_bytes)
		for i in range(num_bytes):
			bv = 0
			for j in range(8):
				bv += bv
				if (i*8)+j < self.num_bits:
					map = self.bit_remap[(i*8)+j]
					bv += (self.buffer[map[0]][map[1]] >> map[2]) & 1
			out_bytes[i] = bv
		return out_bytes

	async def _write_data_start(self, length):
		try:
			packet = b'\x08DATS' + length.to_bytes(2,'big') + b'\x00\x00'
			await self.client.write_gatt_char(CHAR_CMD, encrypt(pad(packet)))
			#await asyncio.sleep(0.01) # Hack because I cba to wait for DATSOK
		except BleakError as e:
			print(e)
			await self.client.disconnect()

	async def _write_data_end(self, wait_response):
		try:
			if not USE_HAX:
				await self.client.write_gatt_char(CHAR_CMD, encrypt(pad(b'\x05DATCP')))
				#await asyncio.sleep(0.01) # Hack because I cba to wait for DATCPOK
			await self.client.write_gatt_char(CHAR_CMD, encrypt(pad(b'\x05MODE\x01')), response=wait_response)
			#await asyncio.sleep(0.005)
		except BleakError as e:
			print(e)
			await self.client.disconnect()

	async def _write_more_data(self, data):
		write_amount = min(len(data), 15)
		try:
			packet = write_amount.to_bytes(1,'big') + data[:write_amount]
			await self.client.write_gatt_char(CHAR_DAT, encrypt(pad(packet)))
		except BleakError as e:
			print(e)
			await self.client.disconnect()
		return write_amount

	async def _start_notify_ack(self):
		try:
			await self.client.start_notify(CHAR_ACK, ack_handler)
		except BleakError as e:
			print(e)
			await self.client.disconnect()

	async def _stop_notify_ack(self):
		try:
			await self.client.stop_notify(CHAR_ACK)
		except BleakError as e:
			print(e)
			await self.client.disconnect()

	def _disconnect_unexpected(self, cbclient=None):
		if self.is_connected:
			self.is_connected = False
			print("Disconnected unexpectedly")
