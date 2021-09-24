import ledmask as ledmask
import asyncio, time, math
import displays

USE_CLASSES = [
	displays.DisplayDSD,
	displays.DisplayVirtualDSD
]

async def boing(display):
	tref = time.time()
	while display.is_connected:
		await asyncio.gather(
			boing_frame(display, time.time() - tref),
			asyncio.sleep(1/display.max_fps)
		)

last_synced = 0
async def boing_frame(display, time_sec):
	draw_background(display, time_sec)
	draw_foreground(display, time_sec)
	do_sync = (time_sec - last_synced) > 5
	if do_sync:
		last_sync = time_sec
	await display.send(do_sync)

def draw_background(display, time_sec):
	display.clear()
	for j in range(display.height//2):
		parallax = (display.width+8*j) / display.width
		for i in range(display.width):
			pos = (i - display.width/2) / (3 * parallax) + 3.5*time_sec
			color = 1 if (pos % 2) < 1 else 0
			#if j >= display.height/6 and j <= display.height/3:
			#	color = 1-color
			display.buffer[i][j+display.height//2] = color

def draw_foreground(display, time_sec):
	radius = 3.3
	radiusi = 4
	shadeoff = 1
	ball_x = map(math.sin(time_sec/0.7), -1, 1, display.width*0.1+radius, display.width*0.9-radius)
	ball_y = map(abs(math.sin(time_sec*3.5))**1.5, 0, 1, display.height*0.85-radius, radius-0.5)
	for i in range(math.floor(ball_x-radiusi), math.ceil(ball_x+radiusi)+1):
		if i < 0 or i >= display.width:
			continue
		for j in range(math.floor(ball_y-radiusi), math.ceil(ball_y+radiusi)+1):
			if j < 0 or j >= display.height:
				continue
			d = ((i-ball_x)**2) + ((j-ball_y)**2)
			d2 = ((i+shadeoff-ball_x)**2) + ((j+shadeoff-ball_y)**2)
			if d <= radius**2:
				display.buffer[i][j] = 1 if (d >= (radius-1)**2 or d2 <= (radius-1.5)**2) else 0

def lerp(a, b, f):
	return a + (b-a)*f

def map(x, in_a, in_b, out_a, out_b):
	return lerp(out_a, out_b, (x-in_a)/(in_b-in_a))

async def run():
	display = await ledmask.find_and_connect(classes=USE_CLASSES)
	if not display:
		return
	await boing(display)
	await display.disconnect()

loop = asyncio.get_event_loop()
loop.run_until_complete(run())
