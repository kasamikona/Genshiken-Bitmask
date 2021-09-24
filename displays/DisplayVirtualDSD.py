from .Display import Display
import asyncio

import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame

import time
import math

USE_HAX = True
SCALE = 10

USE_LED_COLORS = False
LED_COLORS = [(239,63,255), (0,63,255), (223,239,239), (0,239,95)]

class DisplayVirtualDSD(Display):
	def __init__(self):
		super().__init__()
		self.width = 48
		self.height = 12
		self.color = False
		self.bit_depth = 1
		self.buffer = self.buffer = [[0]*self.height for x in range(self.width)]
		self.max_fps = 10 if USE_HAX else 7.5 # Measured up to 10.5 fps with hax, 8.0 without
		self.is_connected = True
		# pygame stuff
		self.pg_screen = pygame.Surface((48, 12), pygame.SRCALPHA, 32)
		self.pg_window = pygame.display.set_mode((self.width*SCALE, self.height*SCALE), pygame.DOUBLEBUF)
		pygame.display.set_caption("Virtual Display Output")
		#pygame.mouse.set_visible(False)
		loop = asyncio.get_event_loop()
		loop.create_task(self._pygame_check_running())

	@classmethod
	async def connect(cls, addresses=None):
		disp = cls()
		print("Connected to virtual DSD display")
		return disp

	async def disconnect(self):
		if not self.is_connected:
			return

		self.is_connected = False
		pygame.display.quit()
		print("Disconnected")

	async def prepare(self):
		for x in range(self.width):
			for y in range(self.height):
				self.buffer[x][y] = 0

	async def send(self, wait_response=False):
		if not self.is_connected:
			return
		self.pg_screen.fill((10,10,10) if USE_LED_COLORS else (0,0,0))
		for x in range(self.width):
			for y in range(self.height):
				if self.buffer[x][y] > 0:
					color = (255, 255, 255)
					if USE_LED_COLORS:
						color = LED_COLORS[(x * len(LED_COLORS)) // self.width]
					self.pg_screen.set_at((x, y), color)
		resized_screen = pygame.transform.scale(self.pg_screen, (self.width*SCALE, self.height*SCALE))
		self.pg_window.blit(resized_screen, (0, 0))
		pygame.display.flip()

		await asyncio.sleep(1/self.max_fps)

	async def wait_for_finish(self):
		pass

	async def _pygame_check_running(self):
		while self.is_connected:
			keys = pygame.key.get_pressed()
			event = pygame.event.poll()
			if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
				await self.disconnect()
			await asyncio.sleep(0.01)

