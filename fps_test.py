import ledmask as ledmask
import asyncio, time, math
import displays

async def fps_test():
	client = ledmask.client
	display = ledmask.display

	test_frames = 1000
	sync_interval = 100

	start_time = time.time()
	radius = (display.height) / 4
	rsq = radius ** 2

	for fn in range(test_frames):
		cx = (fn / 3) % display.width
		cy = display.height - radius - (display.height - 2 * radius) * abs(math.sin(fn / 3))

		for i in range(display.width):
			for j in range(display.height):
				dx = i - cx
				dy = j - cy
				dsq = dx ** 2 + dy ** 2
				display.buffer[i][j] = (2**display.bit_depth)-1 if dsq <= rsq else 0

		if (fn % 10) == 0:
			print("Generated frame", fn)

		await display.send(client, (fn % sync_interval) == 0)

	await display.wait_for_finish(client)
	time_taken = time.time() - start_time

	print("Displayed %s frames in %s seconds, syncing every %s frames" % (test_frames, time_taken, sync_interval))
	print("Measured fps", test_frames / time_taken)

async def run():
	if not await ledmask.connect([displays.DisplayDSD]):
		return
	try:
		await fps_test()
		await ledmask.disconnect()
	except KeyboardInterrupt:
		print("\nInterrupted, connection not closed!")
		print("You may need to power-cycle the display and/or BLE adapter to connect again.")

loop = asyncio.get_event_loop()
loop.run_until_complete(run())
