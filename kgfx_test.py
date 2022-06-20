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
	def __init__(self, size, speed, distx, disty):
		super().__init__()
		self.size = size
		self.speed = speed
		self.distx = distx
		self.disty = disty

	def render(self, out, ins, t_global, t_global_f, t_effect):
		for x in range(out.width):
			for y in range(out.height):
				out.buffer[x][y] = \
					(math.floor((x+self.distx*math.sin(t_global*self.speed))/self.size)&1) ^\
					(math.floor((y+self.disty*math.cos(t_global*self.speed))/self.size)&1)

class E_Mirror(kgfx.Effect):
	def __init__(self, speed, dist):
		super().__init__()
		self.speed = speed
		self.dist = dist
	
	def render(self, out, ins, t_global, t_global_f, t_effect):
		inbuf = ins[0].buffer
		inw = ins[0].width
		outbuf = out.buffer
		mirrx = math.floor(out.width*(0.5+(min(0.5*self.dist,0.4999)*math.sin(t_global*self.speed))))
		for x in range(out.width):
			sampx = abs(x-mirrx)
			for y in range(out.height):
				outbuf[x][y] = inbuf[sampx][y]

class E_Genshiken(kgfx.Effect):
	def __init__(self):
		super().__init__()
		self.imagedata = [ \
			[2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,2,2,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,2], \
			[0,0,1,1,1,0,0,1,1,0,0,1,1,1,0,0,0,1,1,1,0,1,0,0,0,0,1,0,1,0,1,0,0,0,1,1,0,0,1,1,1,0,0], \
			[0,1,0,0,0,0,1,0,0,1,0,1,0,0,1,0,1,0,0,0,0,1,1,1,0,0,0,0,1,1,1,0,0,1,0,0,1,0,1,0,0,1,0], \
			[0,1,0,0,1,0,1,1,1,1,0,1,0,0,1,0,0,0,0,1,0,1,0,0,1,0,1,0,1,0,0,1,0,1,1,1,1,0,1,0,0,1,0], \
			[0,0,1,1,1,0,0,1,0,0,0,1,0,0,1,0,1,1,1,0,0,1,0,0,1,0,1,0,1,0,0,1,0,0,1,0,0,0,1,0,0,1,0], \
			[2,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0], \
		]
	
	def render(self, out, ins, t_global, t_global_f, t_effect):
		for x in range(43):
			if x>=out.width:
				continue
			for y in range(6):
				if y>=out.height:
					continue
				p = self.imagedata[y][x]
				out.buffer[x][y] = p

class E_OverWobble(kgfx.Effect):
	def __init__(self):
		super().__init__()
	
	def render(self, out, ins, t_global, t_global_f, t_effect):
		beat = t_global * 125 / 60
		secondhalf = (math.floor(beat)&63) > 31
		ob = out.buffer
		ib = ins[0].buffer
		iw = ins[0].width
		ih = ins[0].height
		xo = math.sin(math.pi*beat/2)* (5 if secondhalf else 3)
		yo = -math.sin(math.pi*beat)*2
		ysf = -ih/2
		for y in range(out.height):
			ys = math.floor(ysf-yo+ih/2-(out.height-ih)/2+0.5)
			ysf += 1
			xsf = -iw/2
			if secondhalf:
				xsf = (xsf*0.75) + (0.25*math.sin(math.pi*beat))
			for x in range(out.width):
				xs = math.floor(xsf-xo+iw/2-(out.width-iw)/2+0.5)
				if secondhalf:
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

	t_start = time.time()+0.5 # Start 0.5 seconds from now
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
