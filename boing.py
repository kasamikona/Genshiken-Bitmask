import ledmask as ledmask
import asyncio, time, math
import displays

USE_CLASSES = [
	displays.DisplayDSD,
#	displays.DisplayVirtualDSD
]

async def boing(display):
	tref = time.time()
	while display.is_connected:
		await boing_frame(display, time.time() - tref)

async def boing_frame(display, time_sec):
	draw_background(display, time_sec)
	draw_foreground(display, time_sec)
	await display.send(True)

def draw_background(display, time_sec):
	display.clear()
	for j in range(display.height//2):
		parallax = (display.width+8*j) / display.width
		for i in range(display.width):
			pos = ((i - display.width/2) / (3.5 * parallax)) + 3.5*time_sec
			color = 1 if (pos % 2) < 1 else 0
			if j == 0:
				color = 1
			if j > (display.height//4):
				color = 1-color
			display.buffer[i][j+display.height//2] = color

def draw_foreground(display, time_sec):
	movement_x = math.sin(time_sec/0.7)
	movement_y = abs(math.sin(time_sec*3.5))**1.5
	movement_z = math.sin(time_sec/1.3)
	radius = map(movement_z, -1, 1, 2.5, 4)
	shadow_y = map(movement_z, -1, 1, display.height/2, display.height)
	ball_x = map(movement_x, -1, 1, display.width*0.1+radius, display.width*0.9-radius)
	ball_y = map(movement_y, 0, 1, shadow_y-radius, radius/2)
	for i in range(display.width):
		for j in range(display.height):
			ds = ((i-ball_x-1)**2) + ((j-shadow_y)**2)*4
			if ds <= radius**2:
				display.buffer[i][j] = 0
			d = ((i-ball_x)**2) + ((j-ball_y)**2)
			d2 = ((i+1-ball_x)**2) + ((j+1-ball_y)**2)
			if d <= radius**2:
				display.buffer[i][j] = 1 if (d >= (radius-1)**2 or d2 <= (radius-1.5)**2) else 0
				

def lerp(a, b, f):
	return a + (b-a)*f

def map(x, in_a, in_b, out_a, out_b):
	return lerp(out_a, out_b, (x-in_a)/(in_b-in_a))

display = None

async def cleanup():
	global display
	if display and display.is_connected:
		await display.disconnect()

async def run():
	global display
	display = await ledmask.find_and_connect(classes=USE_CLASSES)
	if not display:
		return
	await boing(display)

loop = asyncio.new_event_loop()
try:
	loop.run_until_complete(run())
except KeyboardInterrupt:
	print("Stopped by keyboard interrupt")
finally:
	loop.run_until_complete(cleanup())
