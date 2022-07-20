#!/usr/bin/env python3
import asyncio,math,sys,os,time,ledmask,displays,kgfx

USE_CLASSES=[
	displays.DisplayDSD,
	displays.DisplayVirtualDSD
]

USE_ADDRESSES=[
	"00:2A:EC:00:A0:D6", # ksk
	"00:2A:00:00:A9:F4", # stg7
]

from effects.demofx import ClearBuffer,GenshikenLogo,FadeDither,FadeScanlines,\
	BitmaskLogo,Stains,RegularPolygon,Metaballs,Scroller,Rotozoomer,Greets,\
	Life,Twister,BadApple,Wipe,DropDown

testscene=None
display=None

async def rundemo():
	global display,testscene
	testscene=kgfx.SceneAnimator("demo.story",[ClearBuffer,GenshikenLogo,
		FadeDither,FadeScanlines,BitmaskLogo,Stains,RegularPolygon,Metaballs,
		Scroller,Rotozoomer,Greets,Life,Twister,BadApple,Wipe,DropDown])
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
	classes = USE_CLASSES[:]
	addresses = USE_ADDRESSES[:]
	if 'HWONLY' in os.environ:
		classes = [displays.DisplayDSD]
	if 'ADDRESS' in os.environ:
		addresses = [os.environ['ADDRESS'].split(",")]
	display=await ledmask.find_and_connect(classes=classes,addresses=addresses,dispargs={"title":"Bitmask  :  Genshiken 2022  :  Virtual Display Mode"})
	if not display:
		return
	await rundemo()

if __name__=="__main__":
	os.system('')
	abspath = os.path.abspath(__file__)
	dname = os.path.dirname(abspath)
	os.chdir(dname)
	loop=asyncio.new_event_loop()
	try:
		loop.run_until_complete(run())
		loop.run_until_complete(cleanup())
	except KeyboardInterrupt:
		print("Stopped by keyboard interrupt! You may need to restart the display device and/or bluetooth adapter to connect again.")
		exit()
