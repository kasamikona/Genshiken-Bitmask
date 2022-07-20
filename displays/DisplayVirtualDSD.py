import os,time,math,asyncio
from subprocess import Popen,PIPE,DEVNULL
from .Display import Display

BIGGER  =False
SHOWDOTS=True

class DisplayVirtualDSD(Display):
	def __init__(self, title="Virtual Display Output"):
		super().__init__()
		self.width = 48
		self.height = 12
		self.color = False
		self.bit_depth = 1
		self.buffer = [[0]*self.height for x in range(self.width)]
		self.max_fps = 10
		vfilt = "scale=%s:flags=neighbor"%("960x240"if BIGGER else"480x120")
		if SHOWDOTS:
			vfilt="scale=%s,curves=all='0/0 .1/.2 .8/1',split[a][b];[b]boxblur=%d,format=gbrp[b];[b][a]blend=all_mode=screen:shortest=1"%(("970x250",8)if BIGGER else("485x125",4))
		vsize="97x25"if SHOWDOTS else"48x12"
		command=["ffmpeg","-loglevel","fatal","-hide_banner","-f","rawvideo","-pix_fmt","gray",
			"-s",vsize,"-framerate","30","-re","-i","-","-vf",vfilt,"-pix_fmt","rgb24","-f","sdl",title]
		self.ffprocess=Popen(command,stdout=DEVNULL,stderr=DEVNULL,stdin=PIPE,bufsize=(485 if SHOWDOTS else 288))
		print("Connected to virtual DSD display")
		self.is_connected=True

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
		for x in range(48):
			for y in range(12):
				self.buffer[x][y] = 0

	async def send(self, wait_response=False):
		if not self.is_connected:
			return

		ta = time.time()

		bytes_out = [0]*((97*25) if SHOWDOTS else (48*12))
		p = 98 if SHOWDOTS else 0

		for y in range(12):
			for x in range(48):
				bytes_out[p] = ((1 if self.buffer[x][y]>=0.5 else 0)*255)&255
				p += 2 if SHOWDOTS else 1
			p += 98 if SHOWDOTS else 0

		if self.ffprocess.poll() != None:
			self.is_connected = False
			print("Disconnected by output")
			return
		self.ffprocess.stdin.write(bytes(bytes_out))

		tb = time.time()
		waitfps = 11
		twait = (1/waitfps) - (tb-ta)
		if twait > 0:
			await asyncio.sleep(twait)

	async def wait_for_finish(self):
		pass

