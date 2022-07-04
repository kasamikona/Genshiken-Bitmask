import ledmask as ledmask
import displays
import asyncio, math, sys, os, time
import kgfx

USE_CLASSES = [
	displays.DisplayDSD,
	displays.DisplayVirtualDSD
]

os.system('')

class E_Checkerboard(kgfx.Effect):
	def __init__(self, tstart):
		super().__init__(tstart)
		self.parameters["size"] = 2
		self.parameters["speed"] = 0
		self.parameters["distx"] = 0
		self.parameters["disty"] = 0

	def render(self, out, ins, t, t_global, t_frame):
		p = self.parameters
		size = p["size"]
		speed = p["speed"]
		distx = p["distx"]
		disty = p["disty"]
		for x in range(out.width):
			for y in range(out.height):
				out.buffer[x][y] = \
					(math.floor((x+distx*math.sin(t*speed))/size)&1) ^\
					(math.floor((y+disty*math.cos(t*speed))/size)&1)

class E_Mirror(kgfx.Effect):
	def __init__(self, tstart):
		super().__init__(tstart)
		p = self.parameters
		p["speed"] = 0
		p["dist"] = 0
	
	def render(self, out, ins, t, t_global, t_frame):
		p = self.parameters
		speed = p["speed"]
		dist = p["dist"]
		inbuf = ins[0].buffer
		inw = ins[0].width
		outbuf = out.buffer
		mirrx = math.floor(out.width*(0.5+(min(0.5*dist,0.4999)*math.sin(t*speed))))
		for x in range(out.width):
			sampx = abs(x-mirrx)
			for y in range(out.height):
				outbuf[x][y] = inbuf[sampx][y]

class E_Genshiken(kgfx.Effect):
	def __init__(self, tstart):
		super().__init__(tstart)
		self.imagedata = [ \
			[2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,2,2,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,2], \
			[0,0,1,1,1,0,0,1,1,0,0,1,1,1,0,0,0,1,1,1,0,1,0,0,0,0,1,0,1,0,1,0,0,0,1,1,0,0,1,1,1,0,0], \
			[0,1,0,0,0,0,1,0,0,1,0,1,0,0,1,0,1,0,0,0,0,1,1,1,0,0,0,0,1,1,1,0,0,1,0,0,1,0,1,0,0,1,0], \
			[0,1,0,0,1,0,1,1,1,1,0,1,0,0,1,0,0,0,0,1,0,1,0,0,1,0,1,0,1,0,0,1,0,1,1,1,1,0,1,0,0,1,0], \
			[0,0,1,1,1,0,0,1,0,0,0,1,0,0,1,0,1,1,1,0,0,1,0,0,1,0,1,0,1,0,0,1,0,0,1,0,0,0,1,0,0,1,0], \
			[2,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0], \
		]
	
	def render(self, out, ins, t, t_global, t_frame):
		for x in range(43):
			if x>=out.width:
				continue
			for y in range(6):
				if y>=out.height:
					continue
				p = self.imagedata[y][x]
				out.buffer[x][y] = p

class E_OverWobble(kgfx.Effect):
	def __init__(self, tstart):
		super().__init__(tstart)
		self.parameters["wobble"] = 1
	
	def render(self, out, ins, t, t_global, t_frame):
		beat = t * 125 / 60
		wobble = self.parameters["wobble"] #(math.floor(beat)&63) > 31
		ob = out.buffer
		ib = ins[0].buffer
		iw = ins[0].width
		ih = ins[0].height
		xo = math.sin(math.pi*beat/2)* (5 if wobble else 3)
		yo = -math.sin(math.pi*beat)*2
		ysf = -ih/2
		for y in range(out.height):
			ys = math.floor(ysf-yo+ih/2-(out.height-ih)/2+0.5)
			ysf += 1
			xsf = -iw/2
			if wobble:
				xsf = (xsf*0.75) + (0.25*math.sin(math.pi*beat))
			for x in range(out.width):
				xs = math.floor(xsf-xo+iw/2-(out.width-iw)/2+0.5)
				if wobble:
					xsf += 0.75 + (0.25*math.sin((math.pi*beat)+(x/4)))
				else:
					xsf += 1
				if xs < 0 or ys < 0 or xs >= iw or ys >= ih:
					continue
				p = ib[xs][ys]
				if p < 2:
					ob[x][y] = p

testscene = None
display = None

async def kgfx_test():
	global display, testscene

	testscene = kgfx.SceneAnimator("test.story", [E_Checkerboard, E_Mirror, E_Genshiken, E_OverWobble])

	t_start = time.time()+1 # Start 1 second from now
	running = True

	while running:
		t = time.time() - t_start
		if not testscene.update(t):
			running = False
			break
		final_layer = testscene.render(t)
		if final_layer:
			display.buffer = final_layer.buffer

		if display.is_connected:
			await display.send(True)
		else:
			running = False
			break

async def cleanup():
	global display, testscene
	if display and display.is_connected:
		await display.wait_for_finish()
		await display.disconnect()
	if testscene:
		testscene.cleanup()

async def run():
	global display
	dispargs = {}
	dispargs["title"] = "Funky!"
	display = await ledmask.find_and_connect(classes=USE_CLASSES,dispargs=dispargs)
	if not display:
		return
	await kgfx_test()

if __name__ == "__main__":
	loop = asyncio.new_event_loop()
	try:
		loop.run_until_complete(run())
	except KeyboardInterrupt:
		print("Stopped by keyboard interrupt")
	finally:
		loop.run_until_complete(cleanup())
