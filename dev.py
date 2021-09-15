#! /usr/bin/env python

import pygame
import time
import math

windowwidth = 48 * 10
windowheight = 12 * 10
fps = 10
matrix = [[0 for col in range(48)] for row in range(12)]

screen = pygame.Surface((48, 12), pygame.SRCALPHA, 32)
window = pygame.display.set_mode((windowwidth, windowheight), pygame.NOFRAME)
pygame.display.set_caption("LED dev app")
pygame.mouse.set_visible(False)

running = True

startDate = time.time()
curTime = startDate
frame = 0
drawFrame = True

def testEffect(curTime, frame):
	x = frame % 48
	y = int(math.sin(curTime) * 6 + 6)
	matrix[y][x] = 1

def drawMatrix():
	for x in range(48):
		for y in range(12):
			if matrix[y][x] == 1:
				pygame.draw.polygon(screen, (255, 255, 255), ((x, y), (x, y), (x, y), (x, y)))

while running:
	keys = pygame.key.get_pressed()
	event = pygame.event.poll()
	if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
		running = False

	if drawFrame:
		pygame.display.set_caption("LED dev -- frame " + str(frame))
		testEffect(curTime, frame)
		drawMatrix()
		drawFrame = False

	newTime = time.time()
	curFrame = math.floor((newTime - startDate) * fps)
	if curFrame > frame:
		matrix = [[0 for col in range(48)] for row in range(12)]
		screen.fill((0, 0, 0))
		curTime = newTime
		frame = curFrame
		drawFrame = True

	resized_screen = pygame.transform.scale(screen, (windowwidth, windowheight))
	window.blit(resized_screen, (0, 0))
	pygame.display.flip()

