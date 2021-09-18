import ledmask as ledmask
import asyncio
import displays

def direct_map(self, bit):
	return (bit, 0, 0)

async def bit_test():
	client = ledmask.client
	zombie_display = ledmask.display

	# this worked first try and it was just as much of a wtf moment as you think it was
	class PatchedDisplay(type(zombie_display)):
		def __init__(self):
			super().__init__()
			self.width = 64
			self.height = 1
			self.bit_depth = 1
			super().generate_buffer()
		def reverse_map_bit(self, bit):
			return (bit, 0, 0)

	display = PatchedDisplay()

	print("Display class patched")

	print("One bit at a time")
	await display.clear(client, send=True, wait_response=True)
	for i in range(64):
		display.buffer[i][0] = 1
		await display.send(client)
		await asyncio.sleep(1/display.max_fps)
		display.buffer = [[0] for j in range(64)]

	print("Filling")
	await display.clear(client, send=True, wait_response=True)
	for i in range(64):
		display.buffer[i][0] = 1
		await display.send(client)
		await asyncio.sleep(1/display.max_fps)

async def run():
	if not await ledmask.connect(): # any class is ok
		return
	await bit_test()
	await ledmask.disconnect()

loop = asyncio.get_event_loop()
loop.run_until_complete(run())
