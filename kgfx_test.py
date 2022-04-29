import kgfx
import pygame, math, sys, os
from timeit import default_timer as timer

os.system('')

class E_Checkerboard(kgfx.Effect):
	def __init__(self, size, speed):
		super().__init__()
		self.size = size
		self.speed = speed

	def render(self, out, ins, t_global, t_global_f, t_event):
		for x in range(out.width):
			for y in range(out.height):
				out.buffer[x][y] = (math.floor((x+t_global*self.speed)/self.size)&1) ^ (math.floor(y/self.size)&1)

class E_Mirror(kgfx.Effect):
	def __init__(self):
		super().__init__()
	
	def render(self, out, ins, t_global, t_global_f, t_event):
		for x in range(out.width//2, out.width):
			for y in range(out.height):
				out.buffer[x][y] = out.buffer[out.width-1-x][y]

testscene = kgfx.Scene()
testscene.layers.append(kgfx.Layer(48, 12))
testscene.events.append(kgfx.Event(E_Checkerboard(4,20), 0))
testscene.events.append(kgfx.Event(E_Mirror(), 0))
testscene.compositing_list.append((0, 0, []))
testscene.compositing_list.append((1, 0, []))
testscene.final_layer = 0

screen = pygame.Surface((48, 12), pygame.SRCALPHA, 32)
window = pygame.display.set_mode((480, 120))#, pygame.NOFRAME)

running = True
fps = 10
frame = 0

while running:
	keys = pygame.key.get_pressed()
	event = pygame.event.poll()
	if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
		running = False

	demoTime = timer()
	curFrame = math.floor(demoTime * fps)
	if curFrame > frame:
		screen.fill((0, 0, 0))
		frame = curFrame
		final_layer	= testscene.render(demoTime)
		if final_layer:
			fp = "\033[2J\033[;H"
			fp += "+" + "-"*final_layer.width + "+\n"
			for y in range(final_layer.height):
				fp += "|"
				for x in range(final_layer.width):
					if final_layer.buffer[x][y] == 1:
						pygame.draw.polygon(screen, (255, 255, 255), ((x, y), (x, y), (x, y), (x, y)))
						fp += "#"
					else:
						fp += " "
				fp += "|\n"
			fp += "+" + "-"*final_layer.width + "+\n"
			sys.stdout.write(fp)

	resized_screen = pygame.transform.scale(screen, (480, 120))
	window.blit(resized_screen, (0, 0))
	pygame.display.flip()
