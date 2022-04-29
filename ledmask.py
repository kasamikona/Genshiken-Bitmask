import asyncio, threading
import displays

# Update as new displays are added
AUTO_SCAN_CLASSES = [
	displays.DisplayDSD
]

async def find_and_connect(addresses=None, classes=None):
	print("Looking for compatible display")

	if not classes:
		print("No classes specified")
		return None

	display = None
	for cls in classes:
		display = await cls.connect(addresses)
		if display:
			print("Found %s" % cls.__name__)
			return display

	print("No display found. Is it switched on and connected?")
	return None

class FrameBlaster:
	def __init__(self):
		self._stopevent = threading.Event()
		self.runner = None
	
	def start(self, display_classes):
		self.runner = threading.Thread(target=self._run, args=(display_classes, self._stopevent))
		self.runner.daemon = True
		self.runner.start()

	def stop(self):
		self._stopevent.set()
		self.runner.join()

	def _run(self, display_classes, stopevent):
		loop = asyncio.new_event_loop()
		loop.run_until_complete(self._run_async(display_classes, stopevent))
	
	async def _run_async(self, display_classes, stopevent):
		c = 1
		display = await find_and_connect(classes=display_classes)
		if not display:
			return
		for i in range(display.width):
			for j in range(display.height):
				display.buffer[i][j] = (2**display.bit_depth)-1
		while display.is_connected and not stopevent.is_set():
			await display.send(True)
			print("Displayed",c)
			c += 1
		if display.is_connected:
			await display.disconnect()
