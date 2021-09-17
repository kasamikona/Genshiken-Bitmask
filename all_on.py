import ledmask as ledmask
import asyncio
import displays

async def all_on():
	client = ledmask.client
	display = ledmask.display

	for i in range(display.width):
		for j in range(display.height):
			display.buffer[i][j] = (2**display.bit_depth)-1
	await display.send(client, True)
	print("Enjoy your battery drain")

async def run():
	if not await ledmask.connect([displays.DisplayDSD]):
		return
	await all_on()
	await ledmask.disconnect()

loop = asyncio.get_event_loop()
loop.run_until_complete(run())
