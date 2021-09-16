#! /usr/bin/env python

import pygame
import time
import math

windowwidth = 48 * 10
windowheight = 12 * 10
fps = 10
matrix = [[0]*12 for col in range(48)]

screen = pygame.Surface((48, 12), pygame.SRCALPHA, 32)
window = pygame.display.set_mode((windowwidth, windowheight), pygame.NOFRAME)
pygame.display.set_caption("LED dev app")
pygame.mouse.set_visible(False)

def testEffect(curTime, frame):
	x = frame % 48
	y = int(math.sin(curTime) * 6 + 6)
	matrix[x][y] = 1

def drawMatrix():
	for x in range(48):
		for y in range(12):
			if matrix[x][y] == 1:
				pygame.draw.polygon(screen, (255, 255, 255), ((x, y), (x, y), (x, y), (x, y)))

import ledmask, asyncio, displays
async def sendMatrix():
	client = ledmask.client
	display = ledmask.display
	for x in range(48):
		for y in range(12):
			display.buffer[x][y] = matrix[x][y]
	await display.send(client, False)

async def run():
	global matrix
	if not await ledmask.connect([displays.DisplayDSD]):
		return
	running = True

	startDate = time.time()
	curTime = startDate
	frame = 0
	drawFrame = True

	while running:
		keys = pygame.key.get_pressed()
		event = pygame.event.poll()
		if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
			running = False

		newTime = time.time()
		curFrame = math.floor((newTime - startDate) * fps)
		if curFrame > frame:
			matrix = [[0]*12 for col in range(48)]
			screen.fill((0, 0, 0))
			curTime = newTime
			frame = curFrame
			drawFrame = True

		if drawFrame:
			pygame.display.set_caption("LED dev -- frame " + str(frame))
			testEffect(curTime, frame)
			drawMatrix()
			await sendMatrix()
			drawFrame = False

		resized_screen = pygame.transform.scale(screen, (windowwidth, windowheight))
		window.blit(resized_screen, (0, 0))
		pygame.display.flip()
	await ledmask.disconnect()

loop = asyncio.get_event_loop()
loop.run_until_complete(run())
