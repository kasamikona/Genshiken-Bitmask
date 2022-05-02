import ledmask as ledmask
import asyncio, time, math
import displays

USE_CLASSES = [
	displays.DisplayDSD,
	displays.DisplayVirtualDSD
]

loop = asyncio.new_event_loop()
blaster = ledmask.FrameBlaster()
try:
	blaster.start(USE_CLASSES)
	while blaster.runner.is_alive():
		time.sleep(0.1)
except KeyboardInterrupt:
	print("Stopped by keyboard interrupt")
finally:
	blaster.stop()
