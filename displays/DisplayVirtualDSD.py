import os,time,math,asyncio
from subprocess import Popen, PIPE, DEVNULL
from .Display import Display

USE_HAX = True
SCALE = 10

class DisplayVirtualDSD(Display):
	def __init__(self, title="Virtual Display Output"):
		super().__init__()
		self.width = 48
		self.height = 12
		self.color = False
		self.bit_depth = 1
		self.buffer = [[0]*self.height for x in range(self.width)]
		self.max_fps = 10 if USE_HAX else 7.5 # Measured up to 10.5 fps with hax, 8.0 without
		command = ["ffmpeg","-loglevel","fatal","-hide_banner","-f","rawvideo","-pix_fmt","gray",
			"-s","48x12","-framerate","30","-re","-i","-","-vf","scale=480x120:flags=neighbor",
			"-pix_fmt","rgb24","-f","sdl",title]
		print(" ".join(command))
		self.ffprocess = Popen(command, stdout=DEVNULL, stderr=DEVNULL, stdin=PIPE, bufsize=48*12//2)
		print("Connected to virtual DSD display")
		self.is_connected = True

	@classmethod
	async def connect(cls, addresses=None, dispargs=None):
		disp = cls(dispargs["title"])
		return disp

	async def disconnect(self):
		if not self.is_connected:
			return

		self.ffprocess.terminate()
		self.is_connected = False
		print("Disconnected")

	async def prepare(self):
		for x in range(self.width):
			for y in range(self.height):
				self.buffer[x][y] = 0

	async def send(self, wait_response=False):
		if not self.is_connected:
			return

		ta = time.time()

		bytes_out = [0]*(self.width*self.height)
		p = 0
		for y in range(self.height):
			for x in range(self.width):
				bytes_out[p] = (self.buffer[x][y]*255)&255
				p += 1

		if self.ffprocess.poll() != None:
			self.is_connected = False
			print("Disconnected by output")
			return
		self.ffprocess.stdin.write(bytes(bytes_out))

		tb = time.time()
		twait = (1/self.max_fps) - (tb-ta)
		if twait > 0 and wait_response:
			await asyncio.sleep(twait)

	async def wait_for_finish(self):
		pass

