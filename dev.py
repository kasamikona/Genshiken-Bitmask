#! /usr/bin/env python

import pygame
import time
import math
import random

windowwidth = 48 * 10
windowheight = 12 * 10
fps = 10
matrix = [[0 for col in range(48)] for row in range(12)]
greetsMatrix = [[0 for col in range(48)] for row in range(12)]

logo1 = [ \
	[2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2], \
	[2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2], \
	[2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2], \
	[2,2,2,2,0,0,0,2,2,0,0,2,2,0,0,0,2,2,2,0,0,0,2,0,2,2,2,2,0,2,0,2,0,2,2,2,0,0,2,2,0,0,0,2,2,2,2,2], \
	[2,2,2,0,1,1,1,0,0,1,1,0,0,1,1,1,0,2,0,1,1,1,0,1,0,0,2,0,1,0,1,0,1,0,2,0,1,1,0,0,1,1,1,0,2,2,2,2], \
	[2,2,0,1,0,0,0,0,1,0,0,1,0,1,0,0,1,0,1,0,0,0,0,1,1,1,0,2,0,0,1,1,1,0,0,1,0,0,1,0,1,0,0,1,0,2,2,2], \
	[2,2,0,1,0,0,1,0,1,1,1,1,0,1,0,0,1,0,0,0,0,1,0,1,0,0,1,0,1,0,1,0,0,1,0,1,1,1,1,0,1,0,0,1,0,2,2,2], \
	[2,2,2,0,1,1,1,0,0,1,0,0,0,1,0,0,1,0,1,1,1,0,0,1,0,0,1,0,1,0,1,0,0,1,0,0,1,0,0,0,1,0,0,1,0,2,2,2], \
	[2,2,2,2,0,0,0,2,2,0,2,2,2,0,2,2,0,2,0,0,0,2,2,0,2,2,0,2,0,2,0,2,2,0,2,2,0,2,2,2,0,2,2,0,2,2,2,2], \
	[2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2], \
	[2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2], \
	[2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2], \
]

logo2 = [ \
	[0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0], \
	[0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,1,1,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0], \
	[0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,1,1,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,0,0], \
	[0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,1,1,0,0,0,0,1,0,1,0,0,0,0,0,0,0,1,1,0,0,0,1,1,1,1,1,0,0], \
	[0,0,0,1,1,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,1,1,0,0,1,0,0,0,1,1,0,0,0,0,0,1,1,1,1,0,0,1,1,1,1,0,0,0], \
	[0,0,1,1,1,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,1,0,0,1,0,0,0,1,0,0,0,0,1,1,1,1,1,0,0,0,0,0,1,1,0,0,0], \
	[0,1,1,1,1,0,0,1,0,1,1,1,1,0,0,0,0,0,0,0,0,0,0,1,1,0,1,0,1,0,0,0,0,0,1,1,1,1,0,0,0,0,1,1,0,0,0,0], \
	[0,1,1,1,1,0,0,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,1,1,1,1,0,1,0,0,0,0,0,0,1,1,1,0,0,0,0,1,1,1,0,0,0], \
	[0,0,0,1,1,0,0,1,1,0,1,1,1,0,0,0,0,0,0,0,0,0,0,1,1,1,1,0,1,0,0,0,0,0,0,1,1,0,0,0,0,0,1,1,1,1,0,0], \
	[0,0,0,1,0,0,0,1,1,0,1,1,1,0,0,0,0,0,0,0,0,0,0,1,1,1,1,0,1,0,0,0,0,0,0,1,1,0,0,0,0,1,1,1,1,1,0,0], \
	[0,0,0,1,0,0,0,1,1,1,1,1,1,0,0,0,0,0,0,1,1,0,0,1,0,1,0,0,1,0,0,0,0,0,0,1,1,0,0,0,0,1,0,0,1,1,0,0], \
	[0,0,0,1,0,0,0,1,0,1,0,1,1,0,0,0,0,0,1,1,1,1,0,1,0,1,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,1,0,1,1,1,0], \
	[0,0,0,1,1,0,0,1,0,1,1,1,1,0,0,0,0,1,1,1,1,1,0,1,1,1,1,0,1,0,0,0,0,0,1,1,0,0,0,0,1,0,1,1,1,1,1,1], \
	[0,0,1,1,1,0,0,1,1,1,1,1,1,0,0,0,0,1,1,0,1,0,0,1,1,1,0,0,1,0,0,0,0,0,1,0,0,0,0,0,1,1,1,1,1,1,1,1], \
	[0,1,1,1,1,0,0,1,1,1,1,1,1,0,0,0,1,1,0,0,1,0,1,1,1,1,0,0,1,0,0,0,0,1,1,0,0,1,1,1,1,1,1,1,1,1,0,0], \
	[1,1,1,1,1,0,0,1,1,1,1,1,1,0,0,0,0,0,0,1,1,1,1,1,1,0,1,1,1,0,0,0,0,1,1,0,1,1,1,1,1,1,1,0,1,1,0,0], \
	[1,1,0,1,1,0,0,1,0,1,1,1,1,0,0,0,0,0,0,1,1,1,0,1,1,1,1,1,1,0,0,0,0,1,0,1,1,1,1,1,1,1,0,0,0,1,0,0], \
	[1,1,0,1,1,1,0,1,1,0,1,1,1,0,0,0,0,0,1,1,1,1,0,1,1,1,1,1,1,0,0,0,1,1,0,1,0,1,1,1,1,1,0,0,1,1,0,0], \
	[0,1,1,1,0,1,0,1,1,1,1,1,1,0,0,0,0,0,1,1,1,1,0,1,1,1,1,1,1,0,0,0,1,1,1,0,0,1,1,0,1,1,0,0,1,1,0,0], \
	[0,1,1,1,1,1,0,1,1,1,1,1,1,0,0,0,0,0,1,1,1,0,0,1,1,1,1,0,0,0,0,0,1,1,0,0,0,1,1,0,1,0,0,0,1,1,0,0], \
	[0,1,1,1,1,0,0,1,1,1,1,1,0,0,0,0,0,1,1,1,1,0,0,1,0,1,1,0,0,0,0,0,1,1,0,0,1,1,0,0,1,0,0,0,1,1,0,0], \
	[0,0,1,1,1,0,0,1,0,1,0,0,0,0,0,0,0,1,0,1,1,0,0,0,1,1,1,0,0,0,1,1,0,1,0,0,1,1,0,0,1,0,0,0,1,1,0,0], \
	[0,0,1,1,0,0,0,0,0,1,0,0,0,0,1,0,0,1,0,1,1,0,0,0,1,1,1,0,0,0,1,1,0,1,1,1,1,0,0,0,1,0,0,0,1,1,0,0], \
	[0,1,1,1,0,0,0,0,1,0,0,0,0,0,1,0,1,0,1,1,1,0,0,0,1,1,1,0,0,0,1,0,0,1,1,0,1,0,0,0,1,0,0,0,1,1,0,0], \
	[0,1,1,0,0,0,0,0,1,1,0,0,0,0,1,0,1,1,1,1,1,0,0,1,0,1,1,0,0,0,1,0,0,0,1,0,0,0,0,0,1,0,0,0,1,1,0,0], \
	[1,1,1,0,0,0,0,1,1,1,0,0,0,0,1,0,1,1,1,1,1,0,0,1,0,1,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,0,0,0,1,1,0,0], \
	[1,1,0,0,0,0,0,1,0,1,0,0,0,0,1,1,1,1,0,1,1,0,1,1,0,1,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0], \
	[1,0,0,0,0,0,1,1,0,1,0,0,0,0,1,1,1,0,0,1,1,0,1,0,0,1,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0], \
	[0,0,0,0,0,0,1,0,0,1,0,0,0,0,1,0,0,0,0,1,1,0,1,0,0,1,1,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0], \
	[0,0,0,0,0,0,1,0,0,1,0,0,0,1,1,0,0,0,0,1,1,0,0,0,0,0,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0], \
	[0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,0,0,0,0,0,1,0,0,0,0,0,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0], \
	[0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], \
]

bitmask = [ \
	[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,], \
	[0,0,1,1,0,1,1,1,0,1,1,0,1,1,1,1,1,1,0,1,1,0,0,0,1,0,1,1,0,1,1,1,0,1,1,1,1,1,1,0,1,1,0,0,1,1,0,0,], \
	[0,0,1,1,1,0,0,1,0,1,1,0,0,0,0,0,0,0,0,1,1,0,0,1,1,0,1,1,1,0,0,1,0,1,1,0,0,0,0,0,1,1,0,0,1,1,0,0,], \
	[0,0,1,1,0,0,1,0,0,1,1,0,1,1,1,1,1,1,0,1,1,0,1,0,1,0,1,1,0,0,0,1,0,1,1,1,1,1,1,0,1,1,0,1,1,0,0,0,], \
	[0,0,1,1,1,1,1,1,0,1,1,0,0,0,1,1,0,0,0,1,1,1,1,0,1,0,1,1,1,1,1,1,0,0,0,0,0,1,1,0,1,1,0,1,1,0,0,0,], \
	[0,0,1,1,0,0,0,1,0,1,1,0,0,0,1,1,0,0,0,1,1,0,1,0,1,0,1,1,0,0,0,1,0,1,0,0,1,1,1,0,1,1,1,1,0,0,0,0,], \
	[0,0,1,1,0,0,0,1,0,0,0,0,0,1,1,1,0,0,0,1,1,0,1,0,1,0,1,1,0,0,0,1,0,0,0,1,1,1,0,0,1,1,1,0,0,1,0,0,], \
	[0,0,1,1,0,1,1,0,0,1,1,0,1,1,1,0,0,0,0,1,1,0,1,0,1,0,1,1,0,0,1,0,0,1,1,1,1,0,0,0,1,1,0,0,1,1,0,0,], \
	[0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,], \
	[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,], \
	[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,], \
	[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,], \
]

bitmaskDrips = {0.5: [3, 8], 0.75: [29, 5], 0.9: [41, 8], 1.2: [9, 9], 1.35: [36, 8], 1.5: [22, 8], 1.7: [14, 8], 1.95: [36, 9], 2.05: [3, 9], 2.3: [41, 9], 2.45: [26, 8], 2.7: [9, 10], 2.95: [22, 9], 3.05: [14, 9], 3.2: [3, 10], 3.45: [41, 10], 3.65: [9, 11], 3.9: [36, 10]}
keysBitmaskDrips = list(bitmaskDrips.keys())

charset5 = [None]*256
charset5[31] = [[0]*16]*31
charset5[32] = [[2,2,2,2],[2,2,2,2],[2,2,2,2],[2,2,2,2],[2,2,2,2],[2,2,2,2],[2,2,2,2]]
charset5[33] = [[2,0,2],[0,1,0],[0,1,0],[0,1,0],[2,0,2],[0,1,0],[2,0,2]]
charset5[34] = [[2,0,2,0,2],[0,1,0,1,0],[0,1,0,1,0],[2,0,2,0,2],[2,2,2,2,2],[2,2,2,2,2],[2,2,2,2,2]]
charset5[35] = [[2,2,0,2,0,2,2],[2,0,1,0,1,0,2],[0,1,1,1,1,1,0],[2,0,1,0,1,0,2],[0,1,1,1,1,1,0],[2,0,1,0,1,0,2],[2,2,0,2,0,2,2]]
charset5[36] = [[2,2,0,0,0,0,2],[2,0,1,1,1,1,0],[0,1,0,1,0,0,2],[2,0,1,1,1,0,2],[2,0,0,1,0,1,0],[0,1,1,1,1,0,2],[2,0,0,0,0,2,2]]
charset5[37] = [[2,0,0,2,2,0,2],[0,1,1,0,0,1,0],[0,1,1,0,1,0,2],[2,0,0,1,0,0,2],[2,0,1,0,1,1,0],[0,1,0,0,1,1,0],[2,0,2,2,0,0,2]]
charset5[38] = [[2,2,0,0,2,2,2],[2,0,1,1,0,2,2],[0,1,0,0,1,0,2],[2,0,1,1,1,1,0],[0,1,0,0,1,0,2],[2,0,1,1,0,1,0],[2,2,0,0,2,0,2]]
charset5[39] = [[2,0,2],[0,1,0],[0,1,0],[2,0,2],[2,2,2],[2,2,2],[2,2,2]]
charset5[40] = [[2,2,0,2],[2,0,1,0],[0,1,0,2],[0,1,0,2],[0,1,0,2],[2,0,1,0],[2,2,0,2]]
charset5[41] = [[2,0,2,2],[0,1,0,2],[2,0,1,0],[2,0,1,0],[2,0,1,0],[0,1,0,2],[2,0,2,2]]
charset5[42] = [[2,2,2,0,2,2,2],[2,0,0,1,0,0,2],[0,1,1,1,1,1,0],[2,0,1,1,1,0,2],[2,0,1,0,1,0,2],[2,2,0,2,0,2,2],[2,2,2,2,2,2,2]]
charset5[43] = [[2,2,2,0,2,2,2],[2,2,0,1,0,2,2],[2,0,0,1,0,0,2],[0,1,1,1,1,1,0],[2,0,0,1,0,0,2],[2,2,0,1,0,2,2],[2,2,2,0,2,2,2]]
charset5[44] = [[2,2,2,2],[2,2,2,2],[2,2,2,2],[2,2,0,2],[2,0,1,0],[0,1,0,2],[2,0,2,2]]
charset5[45] = [[2,2,2,2,2,2,2],[2,2,2,2,2,2,2],[2,0,0,0,0,0,2],[0,1,1,1,1,1,0],[2,0,0,0,0,0,2],[2,2,2,2,2,2,2],[2,2,2,2,2,2,2]]
charset5[46] = [[2,2,2,2],[2,2,2,2],[2,2,2,2],[2,0,0,2],[0,1,1,0],[0,1,1,0],[2,0,0,2]]
charset5[47] = [[2,2,2,2,2,0,2],[2,2,2,2,0,1,0],[2,2,2,0,1,0,2],[2,2,0,1,0,2,2],[2,0,1,0,2,2,2],[0,1,0,2,2,2,2],[2,0,2,2,2,2,2]]
charset5[48] = [[2,2,0,0,0,2,2],[2,0,1,1,1,0,2],[0,1,0,0,0,1,0],[0,1,0,1,0,1,0],[0,1,0,0,0,1,0],[2,0,1,1,1,0,2],[2,2,0,0,0,2,2]]
charset5[49] = [[2,2,2,0,2,2,2],[2,0,0,1,0,2,2],[0,1,1,1,0,2,2],[2,0,0,1,0,2,2],[2,0,0,1,0,0,2],[0,1,1,1,1,1,0],[2,0,0,0,0,0,2]]
charset5[50] = [[2,2,0,0,0,2,2],[2,0,1,1,1,0,2],[0,1,0,0,0,1,0],[2,0,0,1,1,0,2],[2,0,1,0,0,0,2],[0,1,1,1,1,1,0],[2,0,0,0,0,0,2]]
charset5[51] = [[2,0,0,0,0,2,2],[0,1,1,1,1,0,2],[2,0,0,0,0,1,0],[2,0,1,1,1,0,2],[2,0,0,0,0,1,0],[0,1,1,1,1,0,2],[2,0,0,0,0,2,2]]
charset5[52] = [[2,2,2,0,0,2,2],[2,2,0,1,1,0,2],[2,0,1,0,1,0,2],[0,1,0,0,1,0,2],[0,1,1,1,1,1,0],[2,0,0,0,1,0,2],[2,2,2,2,0,2,2]]
charset5[53] = [[2,0,0,0,0,0,2],[0,1,1,1,1,1,0],[0,1,0,0,0,0,2],[0,1,1,1,1,0,2],[2,0,0,0,0,1,0],[0,1,1,1,1,0,2],[2,0,0,0,0,2,2]]
charset5[54] = [[2,2,0,0,0,2,2],[2,0,1,1,1,0,2],[0,1,0,0,0,2,2],[0,1,1,1,1,0,2],[0,1,0,0,0,1,0],[2,0,1,1,1,0,2],[2,2,0,0,0,2,2]]
charset5[55] = [[2,0,0,0,0,0,2],[0,1,1,1,1,1,0],[2,0,0,0,0,1,0],[2,2,2,0,1,0,2],[2,2,0,1,0,2,2],[2,2,0,1,0,2,2],[2,2,2,0,2,2,2]]
charset5[56] = [[2,2,0,0,0,2,2],[2,0,1,1,1,0,2],[0,1,0,0,0,1,0],[2,0,1,1,1,0,2],[0,1,0,0,0,1,0],[2,0,1,1,1,0,2],[2,2,0,0,0,2,2]]
charset5[57] = [[2,2,0,0,0,2,2],[2,0,1,1,1,0,2],[0,1,0,0,0,1,0],[2,0,1,1,1,1,0],[2,2,0,0,0,1,0],[2,0,1,1,1,0,2],[2,2,0,0,0,2,2]]
charset5[58] = [[2,0,0,2],[0,1,1,0],[0,1,1,0],[2,0,0,2],[0,1,1,0],[0,1,1,0],[2,0,0,2]]
charset5[59] = [[2,0,0,2],[0,1,1,0],[0,1,1,0],[2,0,0,2],[2,0,1,0],[0,1,0,2],[2,0,2,2]]
charset5[60] = [[2,2,2,2,0,0,2],[2,2,0,0,1,1,0],[2,0,1,1,0,0,2],[0,1,0,0,2,2,2],[2,0,1,1,0,0,2],[2,2,0,0,1,1,0],[2,2,2,2,0,0,2]]
charset5[61] = [[2,2,2,2,2,2,2],[2,0,0,0,0,0,2],[0,1,1,1,1,1,0],[2,0,0,0,0,0,2],[0,1,1,1,1,1,0],[2,0,0,0,0,0,2],[2,2,2,2,2,2,2]]
charset5[62] = [[2,0,0,2,2,2,2],[0,1,1,0,0,2,2],[2,0,0,1,1,0,2],[2,2,2,0,0,1,0],[2,0,0,1,1,0,2],[0,1,1,0,0,2,2],[2,0,0,2,2,2,2]]
charset5[63] = [[2,0,0,0,0,2,2],[0,1,1,1,1,0,2],[2,0,0,0,0,1,0],[2,0,1,1,1,0,2],[2,2,0,0,0,2,2],[2,0,1,0,2,2,2],[2,2,0,2,2,2,2]]
charset5[64] = [[2,2,0,0,0,2,2],[2,0,1,1,1,0,2],[0,1,0,0,0,1,0],[0,1,0,1,1,1,0],[0,1,0,1,1,1,0],[2,0,1,0,0,0,2],[2,2,0,2,2,2,2]]
charset5[65] = [[2,2,0,0,0,2,2],[2,0,1,1,1,0,2],[0,1,0,0,0,1,0],[0,1,1,1,1,1,0],[0,1,0,0,0,1,0],[0,1,0,2,0,1,0],[2,0,2,2,2,0,2]]
charset5[66] = [[2,0,0,0,0,2,2],[0,1,1,1,1,0,2],[0,1,0,0,0,1,0],[0,1,1,1,1,0,2],[0,1,0,0,0,1,0],[0,1,1,1,1,0,2],[2,0,0,0,0,2,2]]
charset5[67] = [[2,2,0,0,0,2,2],[2,0,1,1,1,0,2],[0,1,0,0,0,1,0],[0,1,0,2,2,0,2],[0,1,0,0,0,1,0],[2,0,1,1,1,0,2],[2,2,0,0,0,2,2]]
charset5[68] = [[2,0,0,0,0,2,2],[0,1,1,1,1,0,2],[0,1,0,0,0,1,0],[0,1,0,2,0,1,0],[0,1,0,0,0,1,0],[0,1,1,1,1,0,2],[2,0,0,0,0,2,2]]
charset5[69] = [[2,0,0,0,0,0,2],[0,1,1,1,1,1,0],[0,1,0,0,0,0,2],[0,1,1,1,0,2,2],[0,1,0,0,0,0,2],[0,1,1,1,1,1,0],[2,0,0,0,0,0,2]]
charset5[70] = [[2,0,0,0,0,0,2],[0,1,1,1,1,1,0],[0,1,0,0,0,0,2],[0,1,1,1,0,2,2],[0,1,0,0,2,2,2],[0,1,0,2,2,2,2],[2,0,2,2,2,2,2]]
charset5[71] = [[2,2,0,0,0,2,2],[2,0,1,1,1,0,2],[0,1,0,0,0,0,2],[0,1,0,1,1,1,0],[0,1,0,0,0,1,0],[2,0,1,1,1,0,2],[2,2,0,0,0,2,2]]
charset5[72] = [[2,0,2,2,2,0,2],[0,1,0,2,0,1,0],[0,1,0,0,0,1,0],[0,1,1,1,1,1,0],[0,1,0,0,0,1,0],[0,1,0,2,0,1,0],[2,0,2,2,2,0,2]]
charset5[73] = [[2,0,2],[0,1,0],[0,1,0],[0,1,0],[0,1,0],[0,1,0],[2,0,2]]
charset5[74] = [[2,2,2,2,2,0,2],[2,2,2,2,0,1,0],[2,2,2,2,0,1,0],[2,0,2,2,0,1,0],[0,1,0,0,0,1,0],[2,0,1,1,1,0,2],[2,2,0,0,0,2,2]]
charset5[75] = [[2,0,2,2,2,0,2],[0,1,0,2,0,1,0],[0,1,0,0,1,0,2],[0,1,1,1,0,2,2],[0,1,0,0,1,0,2],[0,1,0,2,0,1,0],[2,0,2,2,2,0,2]]
charset5[76] = [[2,0,2,2,2,2,2],[0,1,0,2,2,2,2],[0,1,0,2,2,2,2],[0,1,0,2,2,2,2],[0,1,0,0,0,0,2],[0,1,1,1,1,1,0],[2,0,0,0,0,0,2]]
charset5[77] = [[2,0,2,2,2,0,2],[0,1,0,2,0,1,0],[0,1,1,0,1,1,0],[0,1,0,1,0,1,0],[0,1,0,1,0,1,0],[0,1,0,1,0,1,0],[2,0,2,0,2,0,2]]
charset5[78] = [[2,0,2,2,2,0,2],[0,1,0,2,0,1,0],[0,1,1,0,0,1,0],[0,1,0,1,0,1,0],[0,1,0,0,1,1,0],[0,1,0,2,0,1,0],[2,0,2,2,2,0,2]]
charset5[79] = [[2,2,0,0,0,2,2],[2,0,1,1,1,0,2],[0,1,0,0,0,1,0],[0,1,0,2,0,1,0],[0,1,0,0,0,1,0],[2,0,1,1,1,0,2],[2,2,0,0,0,2,2]]
charset5[80] = [[2,0,0,0,0,2,2],[0,1,1,1,1,0,2],[0,1,0,0,0,1,0],[0,1,1,1,1,0,2],[0,1,0,0,0,2,2],[0,1,0,2,2,2,2],[2,0,2,2,2,2,2]]
charset5[81] = [[2,2,0,0,0,2,2],[2,0,1,1,1,0,2],[0,1,0,0,0,1,0],[0,1,0,1,0,1,0],[0,1,0,0,1,1,0],[2,0,1,1,1,1,0],[2,2,0,0,0,0,2]]
charset5[82] = [[2,0,0,0,0,2,2],[0,1,1,1,1,0,2],[0,1,0,0,0,1,0],[0,1,1,1,1,0,2],[0,1,0,1,0,0,2],[0,1,0,0,1,1,0],[2,0,2,2,0,0,2]]
charset5[83] = [[2,2,0,0,0,0,2],[2,0,1,1,1,1,0],[0,1,0,0,0,0,2],[2,0,1,1,1,0,2],[2,0,0,0,0,1,0],[0,1,1,1,1,0,2],[2,0,0,0,0,2,2]]
charset5[84] = [[2,0,0,0,0,0,2],[0,1,1,1,1,1,0],[2,0,0,1,0,0,2],[2,2,0,1,0,2,2],[2,2,0,1,0,2,2],[2,2,0,1,0,2,2],[2,2,2,0,2,2,2]]
charset5[85] = [[2,0,2,2,2,0,2],[0,1,0,2,0,1,0],[0,1,0,2,0,1,0],[0,1,0,2,0,1,0],[0,1,0,0,0,1,0],[2,0,1,1,1,0,2],[2,2,0,0,0,2,2]]
charset5[86] = [[2,0,2,2,2,0,2],[0,1,0,2,0,1,0],[0,1,0,2,0,1,0],[2,0,1,0,1,0,2],[2,0,1,0,1,0,2],[2,2,0,1,0,2,2],[2,2,2,0,2,2,2]]
charset5[87] = [[2,0,2,2,2,0,2],[0,1,0,2,0,1,0],[0,1,0,0,0,1,0],[0,1,0,1,0,1,0],[0,1,0,1,0,1,0],[2,0,1,0,1,0,2],[2,2,0,2,0,2,2]]
charset5[88] = [[2,0,2,2,2,0,2],[0,1,0,2,0,1,0],[2,0,1,0,1,0,2],[2,2,0,1,0,2,2],[2,0,1,0,1,0,2],[0,1,0,2,0,1,0],[2,0,2,2,2,0,2]]
charset5[89] = [[2,0,2,2,2,0,2],[0,1,0,2,0,1,0],[0,1,0,2,0,1,0],[2,0,1,0,1,0,2],[2,2,0,1,0,2,2],[2,2,0,1,0,2,2],[2,2,2,0,2,2,2]]
charset5[90] = [[2,0,0,0,0,0,2],[0,1,1,1,1,1,0],[2,0,0,0,1,0,2],[2,2,0,1,0,2,2],[2,0,1,0,0,0,2],[0,1,1,1,1,1,0],[2,0,0,0,0,0,2]]
charset5[91] = [[2,0,0,0,2],[0,1,1,1,0],[0,1,0,0,2],[0,1,0,2,2],[0,1,0,0,2],[0,1,1,1,0],[2,0,0,0,2]]
charset5[92] = [[2,0,2,2,2,2,2],[0,1,0,2,2,2,2],[2,0,1,0,2,2,2],[2,2,0,1,0,2,2],[2,2,2,0,1,0,2],[2,2,2,2,0,1,0],[2,2,2,2,2,0,2]]
charset5[93] = [[2,0,0,0,2],[0,1,1,1,0],[2,0,0,1,0],[2,2,0,1,0],[2,0,0,1,0],[0,1,1,1,0],[2,0,0,0,2]]
charset5[94] = [[2,2,2,0,2,2,2],[2,2,0,1,0,2,2],[2,0,1,0,1,0,2],[0,1,0,2,0,1,0],[2,0,2,2,2,0,2],[2,2,2,2,2,2,2],[2,2,2,2,2,2,2]]
charset5[95] = [[2,2,2,2,2,2,2],[2,2,2,2,2,2,2],[2,2,2,2,2,2,2],[2,2,2,2,2,2,2],[2,0,0,0,0,0,2],[0,1,1,1,1,1,0],[2,0,0,0,0,0,2]]

twister = [[30, 120, 210, 300]] * 48

screen = pygame.Surface((48, 12), pygame.SRCALPHA, 32)
window = pygame.display.set_mode((windowwidth, windowheight), pygame.NOFRAME)
pygame.display.set_caption("LED dev app")
pygame.mouse.set_visible(False)

running = True

startDate = time.time()
curTime = startDate
frame = 0
drawFrame = True

######################
### EFFECTS START HERE
######################

def testEffect(demoTime, frame):
	x = frame % 48
	y = int(math.sin(demoTime) * 6 + 6)
	matrix[y][x] = 1

def drawLogo1(demoTime, frame):
	for x in range(48):
		for y in range(12):
			if logo1[y][x] == 0 or logo1[y][x] == 1:
				matrix[y][x] = logo1[y][x]

def drawLogo2(demoTime, frame):
	if frame > 20:
		for x in range(48):
			for y in range(12):
				offset = int((frame - 32) + y)
				if offset >= 0 and offset < 32:
					matrix[y][x] = logo2[offset][x]

def drawBitmask(demoTime, frame):
	for x in range(48):
		for y in range(12):
			matrix[y][x] = bitmask[y][x]
	for k in range(len(keysBitmaskDrips)):
		if demoTime > keysBitmaskDrips[k]:
			matrix[bitmaskDrips[keysBitmaskDrips[k]][1]][bitmaskDrips[keysBitmaskDrips[k]][0]] = 1
	littleDripY1 = 3 + round(math.tan(demoTime % (math.pi / 2)))
	littleDripY2 = 7 + round(math.tan((demoTime + 0.5) % (math.pi / 2)))
	if littleDripY1 < 11:
		matrix[littleDripY1][17] = 1
	if littleDripY2 < 11:
		matrix[littleDripY2][30] = 1

def fadeScanlines(demoTime, frame, startFrame):
	if startFrame <= frame:
		for x in range(48):
			for y in range(12):
				if y % 2 == 1:
					if x < (frame - startFrame) * 2:
						matrix[y][x] = 0
				else:
					if (47 - x) < (frame - startFrame) * 2:
						matrix[y][x] = 0

rotozoomerAtans = [[0 for col in range(96)] for row in range(24)]
def preloadRotozoomer():
	for x in range(96):
		for y in range(24):
			rotozoomerAtans[y - 12][x - 48] = math.atan2(y, x)

def drawDizzyCircleTiles(demoTime, frame):
	angle = frame / 15
	for x in range(48):
		for y in range(12):
			xOffset = x - 24
			yOffset = y - 6
			trigParam = rotozoomerAtans[yOffset][xOffset] + angle
			hypoParam = math.sqrt(yOffset * yOffset + xOffset * xOffset)
			mappedY = round((math.sin(trigParam) * hypoParam) * math.sin(frame / 50))
			mappedX = round((math.cos(trigParam) * hypoParam) * math.sin(frame / 50))
			matrix[y][x] = (mappedX % 8 < 4) ^ (mappedY % 8 >= 4)

def drawRotozoomer(demoTime, frame):
	angle = frame / 15
	for x in range(48):
		for y in range(12):
			xOffset = x - 24
			yOffset = y - 6
			trigParam = math.atan2(yOffset, xOffset) + angle
			hypoParam = math.sqrt(yOffset * yOffset + xOffset * xOffset)
			mappedY = round((math.sin(trigParam) * hypoParam) * math.sin(frame / 50))
			mappedX = round((math.cos(trigParam) * hypoParam) * math.sin(frame / 50))
			matrix[y][x] = (mappedX % 8 < 4) ^ (mappedY % 8 >= 4)

def drawRegularPolygon(demoTime, frame):
	points = []
	
	sides = 3
	if frame > 180:
		sides = 5

	if frame < 60:
		param = 1
	elif frame < 170:
		param = math.cos(math.pi + (frame - 60) / 10) + 2
		if frame >= 150:
			param = param * (170 - frame) / 20
	elif frame < 180:
		param = 0
	else:
		param = math.cos(math.pi + (frame - 180) / 5) + 1

	for i in range(sides):
		x = math.cos(2 * math.pi * (i / sides) + frame / 5) * 6 * param + 24
		y = math.sin(2 * math.pi * (i / sides) + frame / 5) * 6 * param + 6
		if checkDrawOutOfBounds("y", y) and checkDrawOutOfBounds("x", x):
			matrix[int(y)][int(x)] = 1
		points.append([int(x), int(y)])
	drawPolygon(points)

phraseTestScroller = "LOREM IPSUM DOLOR SIT AMET CONSECTETUR ADIPISCING ELIT"
scrchars = []

greetsChars = []
greets = ["ACHIFAIFA", "COLLAPSE", "LFT", "GARGAJ", "IMOBILIS", "MARCAN", "SNS", "SOGA"]
greetsAscii = [[], [], [], [], [], [], [], []]
greetsChars = [[], [], [], [], [], [], [], []]
greetsWidth = [0, 0, 0, 0, 0, 0, 0, 0]

def preloadTestScroller():
	scrascii = []
	for a in phraseTestScroller:
		scrascii.append(ord(a))
	
	for b in scrascii:
		scrchars.append(charset5[b])

def preloadGreets():
	for indexName, name in enumerate(greets):
		for a in name:
			greetsAscii[indexName].append(ord(a))
			if a == "I":
				greetsWidth[indexName] = greetsWidth[indexName] + 2
			else:
				greetsWidth[indexName] = greetsWidth[indexName] + 6

		for b in greetsAscii[indexName]:
			greetsChars[indexName].append(charset5[b])

def drawTestScroller(demoTime, frame):
	scrollerXOffset = 48 - int(demoTime * 15)
	for indexChar, char in enumerate(scrchars):
		if scrollerXOffset + len(char[0]) >= 0:
			scrollerYOffset = int(math.sin(scrollerXOffset / 5) * 5) + 3
			for indexRow, row in enumerate(char):
				for indexPixel, pixel in enumerate(row):
					pixelX = scrollerXOffset + indexPixel
					pixelY = indexRow + scrollerYOffset
					if (pixel == 0 or pixel == 1) and checkDrawOutOfBounds("x", pixelX) and checkDrawOutOfBounds("y", pixelY):
						matrix[pixelY][pixelX] = pixel
		scrollerXOffset = scrollerXOffset + len(char[0]) - 1
		if scrollerXOffset >= 48:
			break

def drawGreets(demoTime, frame):
	if ((frame % 30) / 10) < 1.0 and math.floor(frame / 30) < len(greets):
		name = math.floor(frame / 30)
		greetXOffset = math.floor(24 - (greetsWidth[name] / 2)) - 1
		greetYOffset = 2
		for indexChar, char in enumerate(greetsChars[name]):
			if greetXOffset + len(char[0]) >= 0:
				for indexRow, row in enumerate(char):
					for indexPixel, pixel in enumerate(row):
						pixelX = indexPixel + greetXOffset
						pixelY = indexRow + greetYOffset
						if (pixel == 0 or pixel == 1) and checkDrawOutOfBounds("x", pixelX) and checkDrawOutOfBounds("y", pixelY):
							greetsMatrix[pixelY][pixelX] = pixel
			greetXOffset = greetXOffset + len(char[0]) - 1
	else:
		tempMatrix = [[0 for col in range(48)] for row in range(12)]
		for x in range(48):
			for y in range(12):
				tempSum = 0 # Cell 5 does not count towards total
				if y > 0 and x > 0:
					tempSum = tempSum + greetsMatrix[y - 1][x - 1] # Cell 1
				if y > 0:
					tempSum = tempSum + greetsMatrix[y - 1][x] # Cell 2
				if y > 0 and x < 47:
					tempSum = tempSum + greetsMatrix[y - 1][x + 1] # Cell 3
				if x > 0:
					tempSum = tempSum + greetsMatrix[y][x - 1] # Cell 4
				if x < 47:
					tempSum = tempSum + greetsMatrix[y][x + 1] # Cell 6
				if y < 11 and x > 0:
					tempSum = tempSum + greetsMatrix[y + 1][x - 1] # Cell 7
				if y < 11:
					tempSum = tempSum + greetsMatrix[y + 1][x] # Cell 8
				if y < 11 and x < 47:
					tempSum = tempSum + greetsMatrix[y + 1][x + 1] # Cell 9
				
				# If the cell is alive, then it stays alive if it has either 2 or 3 live neighbors.
				if greetsMatrix[y][x] == 1:
					if tempSum == 2 or tempSum == 3:
						tempMatrix[y][x] = 1
					else:
						tempMatrix[y][x] == 0
				# If the cell is dead, then it springs to life only in the case that it has 3 live neighbors.
				if greetsMatrix[y][x] == 0:
					if tempSum == 3:
						tempMatrix[y][x] = 1
					else:
						tempMatrix[y][x] = 0

		for x in range(48):
			for y in range(12):
				greetsMatrix[y][x] = tempMatrix[y][x]

	for x in range(48):
		for y in range(12):
			matrix[y][x] = greetsMatrix[y][x]

def drawStains(demoTime, frame):
	for x in range(48):
		for y in range(12):
			xOffset = x + math.sin(demoTime * 2.0) * 20
			yOffset = y + math.cos(demoTime * 1.5) * 25
			xElong = 2.5 + math.sin(demoTime * 4.0)
			yElong = 2.5 + math.cos(demoTime * 1.5) * 0.5
			# xOffset = x
			# yOffset = y
			# xElong = 3
			# yElong = 2.5
			matrix[y][x] = (0.5 + (0.5 * math.sin(xOffset / xElong)) + 0.5 + (0.5 * math.sin(yOffset / yElong))) / 2.0;

	dithering()
	
def drawTwister(demoTime, frame):
	param = 0
	for col in range(48):
		if demoTime > 5:
			param = math.sin(demoTime) + (math.sin(demoTime * 2.5) * math.sin(demoTime * 1.5)) + (math.sin((col / 24.0)) * (math.pow(col / 10.0, 2) / 10.0))
		angle1 = (demoTime + param) % (2 * math.pi)
		angle2 = (angle1 + math.pi * 0.5) % (2 * math.pi)
		angle3 = (angle1 + math.pi) % (2 * math.pi)
		angle4 = (angle1 + math.pi * 1.5) % (2 * math.pi)

		# First, calculate the vertexes and see which one is leftmost because we don't have to draw a line from/to it
		angles = [angle1, angle2, angle3, angle4]
		sinList = [math.sin(angle1), math.sin(angle2), math.sin(angle3), math.sin(angle4)]
		cosList = [math.cos(angle1), math.cos(angle2), math.cos(angle3), math.cos(angle4)]
		indexLeftmostVertex = cosList.index(min(cosList))

		# Remove the leftmost vertex and its calculations
		del angles[indexLeftmostVertex]
		del sinList[indexLeftmostVertex]
		del cosList[indexLeftmostVertex]

		# Obtain the rightmost vertex
		indexRightmostVertex = cosList.index(max(cosList))
		rowRightmostVertex = math.floor(sinList[indexRightmostVertex] * 6 + 6)

		#Draw rightmost vertex pixel
		matrix[rowRightmostVertex][col] = cosList[indexRightmostVertex]

		#Draw a line from the rightmost vertex to one of the other remaining two
		vertex1 = 0
		if indexRightmostVertex == 0:
			vertex1 = 1
		rowVertex1 = math.floor(sinList[vertex1] * 6 + 6)
		
		if rowVertex1 < rowRightmostVertex:
			for row in range(rowRightmostVertex - rowVertex1):
				pixelColor = (cosList[vertex1] + (cosList[indexRightmostVertex] - cosList[vertex1]) * (row / (rowRightmostVertex - rowVertex1)) + 1.0) / 2.0
				matrix[rowVertex1 + row][col] = max(pixelColor, 0.0)
		elif rowVertex1 > rowRightmostVertex:
			for row in range(rowVertex1 - rowRightmostVertex):
				pixelColor = (cosList[vertex1] + (cosList[indexRightmostVertex] - cosList[vertex1]) * (((rowVertex1 - rowRightmostVertex) - row) / (rowRightmostVertex - rowVertex1)) + 1.0) / 2.0
				matrix[rowVertex1 - row][col] = max(pixelColor, 0.0)

		#Draw a line from the rightmost vertex to the last one
		vertex2 = 1
		if indexRightmostVertex == 1 or vertex1 == 1:
			vertex2 = 2
		rowVertex2 = math.floor(sinList[vertex2] * 6 + 6)

		if rowVertex2 < rowRightmostVertex:
			for row in range(rowRightmostVertex - rowVertex2):
				pixelColor = (cosList[vertex2] + (cosList[indexRightmostVertex] - cosList[vertex2]) * (row / (rowRightmostVertex - rowVertex2)) + 1.0) /2.0
				matrix[rowVertex2 + row][col] = max(pixelColor, 0.0)
		elif rowVertex2 > rowRightmostVertex:
			for row in range(rowVertex2 - rowRightmostVertex):
				pixelColor = (cosList[vertex2] + (cosList[indexRightmostVertex] - cosList[vertex2]) * (((rowVertex2 - rowRightmostVertex) - row) / (rowRightmostVertex - rowVertex2)) + 1.0) / 2.0
				matrix[rowVertex2 - row][col] = max(pixelColor, 0.0)

		dithering()

# Code shamelessly ported and adapted from https://www.khanacademy.org/computer-programming/metaballs/6209526669246464
pxSize = 1
sumThreshold = 5
numMetaballs = 3
metaballs = []
for ball in range(numMetaballs):
	metaballs.append({
		"x": random.randint(0, 48),
		"y": random.randint(0, 12),
		"r": random.randint(5, 15),
		"vx": random.choice([-2, -1, 1, 2]),
		"vy": random.choice([-2, -1, 1, 2])
		# "vx": random.choice([-2, -1, 0.1, 0.5, 1.5]),
		# "vy": random.choice([-1, -0.25, 1, 2])
	})
def drawMetaballs(demoTime, frame):
	for i in range(numMetaballs):
		c = metaballs[i]

		c["x"] += c["vx"]
		c["y"] += c["vy"]
		
		if c["x"] < 0:
			c["vx"] = +abs(c["vx"])
		
		if c["x"] > 48:
			c["vx"] = -abs(c["vx"])
		
		if c["y"] < 0:
			c["vy"] = +abs(c["vy"])
		
		if c["y"] > 12:
			c["vy"] = -abs(c["vy"])

	for x in range(0, 48, pxSize):
		for y in range(0, 12, pxSize):
			sum = 0
			closestD2 = math.inf;
			closestColor = None;
			for i in range(numMetaballs):
				c = metaballs[i]
				dx = x - c["x"]
				dy = y - c["y"]
				d2 = dx * dx + dy * dy
				if d2 == 0:
					d2 = 0.00001
				sum += c["r"] * c["r"] / d2
			if sum > sumThreshold:
				matrix[y][x] = 1

####################
### EFFECTS END HERE
####################

##################################
### AUXILIARY FUNCTIONS START HERE
##################################

def drawPolygon(points):
	for i in range(len(points)):
		x1 = points[i][0]
		y1 = points[i][1]
		if i == len(points) - 1:
			x2 = points[0][0]
			y2 = points[0][1]
		else:
			x2 = points[i + 1][0]
			y2 = points[i + 1][1]
		
		drawLine(x1, y1, x2, y2)

def drawLine(x1, y1, x2, y2):
	dx = x2 - x1
	dy = y2 - y1

	if abs(dx) > abs(dy):
		if x2 > x1:
			for x in range(x1, x2):
				rampStep = (x - x1) / (x2 - x1)
				y = round((y2 - y1) * rampStep) + y1
				if checkDrawOutOfBounds("y", y) and checkDrawOutOfBounds("x", x):
					matrix[y][x] = 1
		else:
			for x in range(x2, x1):
				rampStep = (x - x2) / (x1 - x2)
				y = round((y1 - y2) * rampStep) + y2
				if checkDrawOutOfBounds("y", y) and checkDrawOutOfBounds("x", x):
					matrix[y][x] = 1
	else:
		if y2 > y1:
			for y in range(y1, y2):
				rampStep = (y - y1) / (y2 - y1)
				x = round((x2 - x1) * rampStep) + x1
				if checkDrawOutOfBounds("y", y) and checkDrawOutOfBounds("x", x):
					matrix[y][x] = 1
		else:
			for y in range(y2, y1):
				rampStep = (y - y2) / (y1 - y2)
				x = round((x1 - x2) * rampStep) + x2
				if checkDrawOutOfBounds("y", y) and checkDrawOutOfBounds("x", x):
					matrix[y][x] = 1

def checkDrawOutOfBounds(coord, value):
	if coord == "x" and (value < 0 or value >= 48):
		return False
	if coord == "y" and (value < 0 or value >= 12):
		return False
	return True

def getGrayFromDepthTwister(pos):
	return round(pos * 224 + 32)

def dithering():
	# ditherMatrix = [[0, 0.5], [0.75, 0.25]] # 2x2 convolution matrix, test
	# ditherMatrix = [[0.125, 0.5], [0.875, 0.25]] # 2x2, another test
	ditherMatrix = [[0, 0.5, 0.125, 0.625], [0.75, 0.25, 0.875, 0.375], [0.1875, 0.6875, 0.0625, 0.5625], [0.9375, 0.4375, 0.8125, 0.3125]]

	n = 4
	for x in range(48):
		for y in range(12):
			i = x % n
			j = y % n
			if matrix[y][x] > ditherMatrix[i][j]:
				matrix[y][x] = 1
			else:
				matrix[y][x] = 0

################################
### AUXILIARY FUNCTIONS END HERE
################################

def drawMatrix():
	for x in range(48):
		for y in range(12):
			if matrix[y][x] == 1:
				pygame.draw.polygon(screen, (255, 255, 255), ((x, y), (x, y), (x, y), (x, y)))

def drawGrayscaleMatrix():
	for x in range(48):
		for y in range(12):
			graytone = round(matrix[y][x] * 255)
			pygame.draw.polygon(screen, (graytone, graytone, graytone), ((x, y), (x, y), (x, y), (x, y)))

preloadRotozoomer()
preloadTestScroller()
preloadGreets()

demoTime = 0

while running:
	keys = pygame.key.get_pressed()
	event = pygame.event.poll()
	if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
		running = False

	newTime = time.time()
	demoTime = newTime - startDate
	curFrame = math.floor(demoTime * fps)
	if curFrame > frame:
		matrix = [[0 for col in range(48)] for row in range(12)]
		screen.fill((0, 0, 0))
		curTime = newTime
		frame = curFrame
		drawFrame = True

	if drawFrame:
		pygame.display.set_caption("LED dev -- frame " + str(frame))

		# drawLogo2(demoTime, frame)
		# drawLogo1(demoTime, frame)
		# fadeScanlines(demoTime, frame, 64)
		# drawBitmask(demoTime, frame)

		# # drawRotozoomer(demoTime, frame)
		# # #drawDizzyCircleTiles(demoTime, frame)

		# drawRegularPolygon(demoTime, frame)

		# # #drawTestScroller(demoTime, frame)

		# # # #drawStains(demoTime, frame)

		# # # # #drawTwister(demoTime, frame)

		# # # # # #drawMetaballs(demoTime, frame)

		drawGreets(demoTime, frame)

		drawMatrix()
		#drawGrayscaleMatrix()
		drawFrame = False

	resized_screen = pygame.transform.scale(screen, (windowwidth, windowheight))
	window.blit(resized_screen, (0, 0))
	pygame.display.flip()

