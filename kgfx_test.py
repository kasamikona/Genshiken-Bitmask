import ledmask as ledmask
import displays
import asyncio, math, sys, os, time
from timeit import default_timer as timer
import kgfx
from subprocess import Popen, PIPE, DEVNULL

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

	def render(self, out, ins, t_global, t_global_f, t_event):
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
	
	def render(self, out, ins, t_global, t_global_f, t_event):
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
	
	def render(self, out, ins, t_global, t_global_f, t_event):
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
	
	def render(self, out, ins, t_global, t_global_f, t_event):
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

testscene = kgfx.Scene()
testscene.layers.append(kgfx.Layer(48, 12)) # Layer 0
testscene.layers.append(kgfx.Layer(48, 12)) # Layer 1
testscene.layers.append(kgfx.Layer(43, 6))  # Layer 2 different size
testscene.events.append(kgfx.Event(E_Checkerboard(5,1,10,8), 0)) # Checkerboard, no inputs
testscene.events.append(kgfx.Event(E_Mirror(1,1), 0)) # Mirror, 1 input
testscene.events.append(kgfx.Event(E_Genshiken(), 0)) # Genshiken logo, no inputs
testscene.events.append(kgfx.Event(E_OverWobble(), 0)) # Over wobble, 1 inputs
testscene.compositing_list.append((0, 1, [])) # Checkerboard -> Layer 1
testscene.compositing_list.append((1, 0, [1])) # Layer 1 -> Mirror -> Layer 0
testscene.compositing_list.append((2, 2, [])) # Genshiken logo -> Layer 2
testscene.compositing_list.append((3, 0, [2])) # Layer 2 -> Over wobble -> Layer 0
testscene.final_layer = 0 # Output layer 0

p_music = None
display = None

async def kgfx_test():
	global display, p_music

	start_time = time.time()
	running = True

	c_music = ["ffplay","-nodisp","-hide_banner","-loop","0","pomcrop.mp3"]
	p_music = Popen(c_music, stdout=DEVNULL, stderr=DEVNULL, stdin=DEVNULL)

	while running:
		demo_time = time.time() - start_time
		final_layer	= testscene.render(demo_time)
		if final_layer:
			display.buffer = final_layer.buffer

		if display.is_connected:
			await display.send(True)
		else:
			print("Test aborted")
			running = False
			break

	await display.wait_for_finish()


async def cleanup():
	global display, p_music
	if display and display.is_connected:
		await display.disconnect()
	if p_music:
		p_music.terminate()

async def run():
	global display
	dispargs = {}
	dispargs["title"] = "Funky!"
	display = await ledmask.find_and_connect(classes=USE_CLASSES,dispargs=dispargs)
	if not display:
		return
	await kgfx_test()
	await display.disconnect()

loop = asyncio.new_event_loop()
try:
	loop.run_until_complete(run())
except KeyboardInterrupt:
	print("Stopped by keyboard interrupt")
finally:
	loop.run_until_complete(cleanup())
