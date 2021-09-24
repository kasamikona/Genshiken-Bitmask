import asyncio

class Display():
	def __init__(self):
		self.width = 0
		self.height = 0
		self.color = False # RGB or monochrome display
		self.bit_depth = 1 # Total bits per pixel
		self.buffer = None # Pixel buffer
		self.max_fps = 0 # Max frame rate the display/connection can handle, should be slightly below measured maximum
		self.is_connected = False

	@classmethod
	async def connect(cls, addresses=None):
		'''
		Attempts to connect to an appropriate device.
		May be given specific addresses to check.
		Returns object: New instance of this display if connected, otherwise None.
		'''
		return None

	async def disconnect(self):
		'''Disconnects the connected device'''
		pass

	async def prepare(self):
		pass

	async def send(self, wait_response=False):
		pass

	async def wait_for_finish(self):
		pass

	def clear(self):
		for x in range(self.width):
			for y in range(self.height):
				self.buffer[x][y] = 0
