import ledmask as ledmask
import asyncio
import displays

USE_CLASSES = [
	displays.DisplayDSD,
	displays.DisplayVirtualDSD
]

async def all_on(display):
	for i in range(display.width):
		for j in range(display.height):
			display.buffer[i][j] = (2**display.bit_depth)-1
	await display.send(True)
	print("Enjoy your battery drain")

async def run():
	display = await ledmask.find_and_connect(classes=USE_CLASSES)
	if not display:
		return
	await all_on(display)
	await display.disconnect()

loop = asyncio.get_event_loop()
loop.run_until_complete(run())
