import asyncio,math,sys,os,time,ledmask,displays,kgfx

USE_CLASSES=[
	displays.DisplayDSD,
	displays.DisplayVirtualDSD
]

USE_ADDRESSES=[
	#"00:2A:EC:00:A0:D6",
]

from effects.testfx import BadApple
from effects.demofx import GenshikenLogo,FadeScanlines,Greets,Life,ClearBuffer

testscene=None
display=None

async def rundemo():
	global display,testscene
	testscene=kgfx.SceneAnimator("test.story",[BadApple,GenshikenLogo,FadeScanlines,Greets,Life,ClearBuffer])
	display.clear()
	await display.send(True)
	await display.send(True)
	await asyncio.sleep(1)
	try:
		t_start = time.time()-float(sys.argv[1])
	except (IndexError, ValueError):
		t_start = time.time()
	running=True
	while running:
		t=time.time()-t_start
		if not testscene.update(t):
			running = False
			break
		final_layer=testscene.render(t)
		if final_layer:
			display.buffer=final_layer.buffer
		if display.is_connected:
			await display.send(True)
		else:
			running=False
			break

async def cleanup():
	global display,testscene
	if display and display.is_connected:
		display.clear()
		await display.send(True)
		await display.wait_for_finish()
		await display.disconnect()
	if testscene:
		testscene.cleanup()

async def run():
	global display
	display=await ledmask.find_and_connect(classes=USE_CLASSES,dispargs={"title":"Bitmask  :  Genshiken 2022  :  Virtual Display Mode"})
	if not display:
		return
	await rundemo()

if __name__=="__main__":
	os.system('')
	loop=asyncio.new_event_loop()
	try:
		loop.run_until_complete(run())
		loop.run_until_complete(cleanup())
	except KeyboardInterrupt:
		print("Stopped by keyboard interrupt! You may need to restart the display device and/or bluetooth adapter to connect again.")
		exit()
