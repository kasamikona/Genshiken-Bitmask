import asyncio,math,sys,os,time,ledmask,displays,kgfx

USE_CLASSES=[
	displays.DisplayDSD,
	displays.DisplayVirtualDSD
]

from effects.testfx import Checkerboard,Mirror,Genshiken,OverWobble,BadApple

testscene=None
display=None

async def rundemo():
	global display,testscene
	testscene=kgfx.SceneAnimator("test.story",[Checkerboard,Mirror,Genshiken,OverWobble,BadApple])
	t_start=time.time()+1
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
		await display.wait_for_finish()
		await display.disconnect()
	if testscene:
		testscene.cleanup()

async def run():
	global display
	display=await ledmask.find_and_connect(classes=USE_CLASSES,dispargs={"title":"Funky"})
	if not display:
		return
	await rundemo()

if __name__=="__main__":
	os.system('')
	loop=asyncio.new_event_loop()
	try:
		loop.run_until_complete(run())
	except KeyboardInterrupt:
		print("Stopped by keyboard interrupt")
	finally:
		loop.run_until_complete(cleanup())
