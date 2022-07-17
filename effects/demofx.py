import math,random,kgfx,os

charset5=[None]*256
charset5[32]=[[2,2,2,2],[2,2,2,2],[2,2,2,2],[2,2,2,2],[2,2,2,2],[2,2,2,2],[2,2,2,2]]
charset5[33]=[[2,0,2],[0,1,0],[0,1,0],[0,1,0],[2,0,2],[0,1,0],[2,0,2]]
charset5[34]=[[2,0,2,0,2],[0,1,0,1,0],[0,1,0,1,0],[2,0,2,0,2],[2,2,2,2,2],[2,2,2,2,2],[2,2,2,2,2]]
charset5[35]=[[2,2,0,2,0,2,2],[2,0,1,0,1,0,2],[0,1,1,1,1,1,0],[2,0,1,0,1,0,2],[0,1,1,1,1,1,0],[2,0,1,0,1,0,2],[2,2,0,2,0,2,2]]
charset5[36]=[[2,2,0,0,0,0,2],[2,0,1,1,1,1,0],[0,1,0,1,0,0,2],[2,0,1,1,1,0,2],[2,0,0,1,0,1,0],[0,1,1,1,1,0,2],[2,0,0,0,0,2,2]]
charset5[37]=[[2,0,0,2,2,0,2],[0,1,1,0,0,1,0],[0,1,1,0,1,0,2],[2,0,0,1,0,0,2],[2,0,1,0,1,1,0],[0,1,0,0,1,1,0],[2,0,2,2,0,0,2]]
charset5[38]=[[2,2,0,0,2,2,2],[2,0,1,1,0,2,2],[0,1,0,0,1,0,2],[2,0,1,1,1,1,0],[0,1,0,0,1,0,2],[2,0,1,1,0,1,0],[2,2,0,0,2,0,2]]
charset5[39]=[[2,0,2],[0,1,0],[0,1,0],[2,0,2],[2,2,2],[2,2,2],[2,2,2]]
charset5[40]=[[2,2,0,2],[2,0,1,0],[0,1,0,2],[0,1,0,2],[0,1,0,2],[2,0,1,0],[2,2,0,2]]
charset5[41]=[[2,0,2,2],[0,1,0,2],[2,0,1,0],[2,0,1,0],[2,0,1,0],[0,1,0,2],[2,0,2,2]]
charset5[42]=[[2,2,2,0,2,2,2],[2,0,0,1,0,0,2],[0,1,1,1,1,1,0],[2,0,1,1,1,0,2],[2,0,1,0,1,0,2],[2,2,0,2,0,2,2],[2,2,2,2,2,2,2]]
charset5[43]=[[2,2,2,0,2,2,2],[2,2,0,1,0,2,2],[2,0,0,1,0,0,2],[0,1,1,1,1,1,0],[2,0,0,1,0,0,2],[2,2,0,1,0,2,2],[2,2,2,0,2,2,2]]
charset5[44]=[[2,2,2,2],[2,2,2,2],[2,2,2,2],[2,2,0,2],[2,0,1,0],[0,1,0,2],[2,0,2,2]]
charset5[45]=[[2,2,2,2,2,2,2],[2,2,2,2,2,2,2],[2,0,0,0,0,0,2],[0,1,1,1,1,1,0],[2,0,0,0,0,0,2],[2,2,2,2,2,2,2],[2,2,2,2,2,2,2]]
charset5[46]=[[2,2,2,2],[2,2,2,2],[2,2,2,2],[2,0,0,2],[0,1,1,0],[0,1,1,0],[2,0,0,2]]
charset5[47]=[[2,2,2,2,2,0,2],[2,2,2,2,0,1,0],[2,2,2,0,1,0,2],[2,2,0,1,0,2,2],[2,0,1,0,2,2,2],[0,1,0,2,2,2,2],[2,0,2,2,2,2,2]]
charset5[48]=[[2,2,0,0,0,2,2],[2,0,1,1,1,0,2],[0,1,0,0,0,1,0],[0,1,0,1,0,1,0],[0,1,0,0,0,1,0],[2,0,1,1,1,0,2],[2,2,0,0,0,2,2]]
charset5[49]=[[2,2,2,0,2,2,2],[2,0,0,1,0,2,2],[0,1,1,1,0,2,2],[2,0,0,1,0,2,2],[2,0,0,1,0,0,2],[0,1,1,1,1,1,0],[2,0,0,0,0,0,2]]
charset5[50]=[[2,2,0,0,0,2,2],[2,0,1,1,1,0,2],[0,1,0,0,0,1,0],[2,0,0,1,1,0,2],[2,0,1,0,0,0,2],[0,1,1,1,1,1,0],[2,0,0,0,0,0,2]]
charset5[51]=[[2,0,0,0,0,2,2],[0,1,1,1,1,0,2],[2,0,0,0,0,1,0],[2,0,1,1,1,0,2],[2,0,0,0,0,1,0],[0,1,1,1,1,0,2],[2,0,0,0,0,2,2]]
charset5[52]=[[2,2,2,0,0,2,2],[2,2,0,1,1,0,2],[2,0,1,0,1,0,2],[0,1,0,0,1,0,2],[0,1,1,1,1,1,0],[2,0,0,0,1,0,2],[2,2,2,2,0,2,2]]
charset5[53]=[[2,0,0,0,0,0,2],[0,1,1,1,1,1,0],[0,1,0,0,0,0,2],[0,1,1,1,1,0,2],[2,0,0,0,0,1,0],[0,1,1,1,1,0,2],[2,0,0,0,0,2,2]]
charset5[54]=[[2,2,0,0,0,2,2],[2,0,1,1,1,0,2],[0,1,0,0,0,2,2],[0,1,1,1,1,0,2],[0,1,0,0,0,1,0],[2,0,1,1,1,0,2],[2,2,0,0,0,2,2]]
charset5[55]=[[2,0,0,0,0,0,2],[0,1,1,1,1,1,0],[2,0,0,0,0,1,0],[2,2,2,0,1,0,2],[2,2,0,1,0,2,2],[2,2,0,1,0,2,2],[2,2,2,0,2,2,2]]
charset5[56]=[[2,2,0,0,0,2,2],[2,0,1,1,1,0,2],[0,1,0,0,0,1,0],[2,0,1,1,1,0,2],[0,1,0,0,0,1,0],[2,0,1,1,1,0,2],[2,2,0,0,0,2,2]]
charset5[57]=[[2,2,0,0,0,2,2],[2,0,1,1,1,0,2],[0,1,0,0,0,1,0],[2,0,1,1,1,1,0],[2,2,0,0,0,1,0],[2,0,1,1,1,0,2],[2,2,0,0,0,2,2]]
charset5[58]=[[2,0,0,2],[0,1,1,0],[0,1,1,0],[2,0,0,2],[0,1,1,0],[0,1,1,0],[2,0,0,2]]
charset5[59]=[[2,0,0,2],[0,1,1,0],[0,1,1,0],[2,0,0,2],[2,0,1,0],[0,1,0,2],[2,0,2,2]]
charset5[60]=[[2,2,2,2,0,0,2],[2,2,0,0,1,1,0],[2,0,1,1,0,0,2],[0,1,0,0,2,2,2],[2,0,1,1,0,0,2],[2,2,0,0,1,1,0],[2,2,2,2,0,0,2]]
charset5[61]=[[2,2,2,2,2,2,2],[2,0,0,0,0,0,2],[0,1,1,1,1,1,0],[2,0,0,0,0,0,2],[0,1,1,1,1,1,0],[2,0,0,0,0,0,2],[2,2,2,2,2,2,2]]
charset5[62]=[[2,0,0,2,2,2,2],[0,1,1,0,0,2,2],[2,0,0,1,1,0,2],[2,2,2,0,0,1,0],[2,0,0,1,1,0,2],[0,1,1,0,0,2,2],[2,0,0,2,2,2,2]]
charset5[63]=[[2,0,0,0,0,2,2],[0,1,1,1,1,0,2],[2,0,0,0,0,1,0],[2,0,1,1,1,0,2],[2,2,0,0,0,2,2],[2,0,1,0,2,2,2],[2,2,0,2,2,2,2]]
charset5[64]=[[2,2,0,0,0,2,2],[2,0,1,1,1,0,2],[0,1,0,0,0,1,0],[0,1,0,1,1,1,0],[0,1,0,1,1,1,0],[2,0,1,0,0,0,2],[2,2,0,2,2,2,2]]
charset5[65]=[[2,2,0,0,0,2,2],[2,0,1,1,1,0,2],[0,1,0,0,0,1,0],[0,1,1,1,1,1,0],[0,1,0,0,0,1,0],[0,1,0,2,0,1,0],[2,0,2,2,2,0,2]]
charset5[66]=[[2,0,0,0,0,2,2],[0,1,1,1,1,0,2],[0,1,0,0,0,1,0],[0,1,1,1,1,0,2],[0,1,0,0,0,1,0],[0,1,1,1,1,0,2],[2,0,0,0,0,2,2]]
charset5[67]=[[2,2,0,0,0,2,2],[2,0,1,1,1,0,2],[0,1,0,0,0,1,0],[0,1,0,2,2,0,2],[0,1,0,0,0,1,0],[2,0,1,1,1,0,2],[2,2,0,0,0,2,2]]
charset5[68]=[[2,0,0,0,0,2,2],[0,1,1,1,1,0,2],[0,1,0,0,0,1,0],[0,1,0,2,0,1,0],[0,1,0,0,0,1,0],[0,1,1,1,1,0,2],[2,0,0,0,0,2,2]]
charset5[69]=[[2,0,0,0,0,0,2],[0,1,1,1,1,1,0],[0,1,0,0,0,0,2],[0,1,1,1,0,2,2],[0,1,0,0,0,0,2],[0,1,1,1,1,1,0],[2,0,0,0,0,0,2]]
charset5[70]=[[2,0,0,0,0,0,2],[0,1,1,1,1,1,0],[0,1,0,0,0,0,2],[0,1,1,1,0,2,2],[0,1,0,0,2,2,2],[0,1,0,2,2,2,2],[2,0,2,2,2,2,2]]
charset5[71]=[[2,2,0,0,0,2,2],[2,0,1,1,1,0,2],[0,1,0,0,0,0,2],[0,1,0,1,1,1,0],[0,1,0,0,0,1,0],[2,0,1,1,1,0,2],[2,2,0,0,0,2,2]]
charset5[72]=[[2,0,2,2,2,0,2],[0,1,0,2,0,1,0],[0,1,0,0,0,1,0],[0,1,1,1,1,1,0],[0,1,0,0,0,1,0],[0,1,0,2,0,1,0],[2,0,2,2,2,0,2]]
charset5[73]=[[2,0,2],[0,1,0],[0,1,0],[0,1,0],[0,1,0],[0,1,0],[2,0,2]]
charset5[74]=[[2,2,2,2,2,0,2],[2,2,2,2,0,1,0],[2,2,2,2,0,1,0],[2,0,2,2,0,1,0],[0,1,0,0,0,1,0],[2,0,1,1,1,0,2],[2,2,0,0,0,2,2]]
charset5[75]=[[2,0,2,2,2,0,2],[0,1,0,2,0,1,0],[0,1,0,0,1,0,2],[0,1,1,1,0,2,2],[0,1,0,0,1,0,2],[0,1,0,2,0,1,0],[2,0,2,2,2,0,2]]
charset5[76]=[[2,0,2,2,2,2,2],[0,1,0,2,2,2,2],[0,1,0,2,2,2,2],[0,1,0,2,2,2,2],[0,1,0,0,0,0,2],[0,1,1,1,1,1,0],[2,0,0,0,0,0,2]]
charset5[77]=[[2,0,2,2,2,0,2],[0,1,0,2,0,1,0],[0,1,1,0,1,1,0],[0,1,0,1,0,1,0],[0,1,0,1,0,1,0],[0,1,0,1,0,1,0],[2,0,2,0,2,0,2]]
charset5[78]=[[2,0,2,2,2,0,2],[0,1,0,2,0,1,0],[0,1,1,0,0,1,0],[0,1,0,1,0,1,0],[0,1,0,0,1,1,0],[0,1,0,2,0,1,0],[2,0,2,2,2,0,2]]
charset5[79]=[[2,2,0,0,0,2,2],[2,0,1,1,1,0,2],[0,1,0,0,0,1,0],[0,1,0,2,0,1,0],[0,1,0,0,0,1,0],[2,0,1,1,1,0,2],[2,2,0,0,0,2,2]]
charset5[80]=[[2,0,0,0,0,2,2],[0,1,1,1,1,0,2],[0,1,0,0,0,1,0],[0,1,1,1,1,0,2],[0,1,0,0,0,2,2],[0,1,0,2,2,2,2],[2,0,2,2,2,2,2]]
charset5[81]=[[2,2,0,0,0,2,2],[2,0,1,1,1,0,2],[0,1,0,0,0,1,0],[0,1,0,1,0,1,0],[0,1,0,0,1,1,0],[2,0,1,1,1,1,0],[2,2,0,0,0,0,2]]
charset5[82]=[[2,0,0,0,0,2,2],[0,1,1,1,1,0,2],[0,1,0,0,0,1,0],[0,1,1,1,1,0,2],[0,1,0,1,0,0,2],[0,1,0,0,1,1,0],[2,0,2,2,0,0,2]]
charset5[83]=[[2,2,0,0,0,0,2],[2,0,1,1,1,1,0],[0,1,0,0,0,0,2],[2,0,1,1,1,0,2],[2,0,0,0,0,1,0],[0,1,1,1,1,0,2],[2,0,0,0,0,2,2]]
charset5[84]=[[2,0,0,0,0,0,2],[0,1,1,1,1,1,0],[2,0,0,1,0,0,2],[2,2,0,1,0,2,2],[2,2,0,1,0,2,2],[2,2,0,1,0,2,2],[2,2,2,0,2,2,2]]
charset5[85]=[[2,0,2,2,2,0,2],[0,1,0,2,0,1,0],[0,1,0,2,0,1,0],[0,1,0,2,0,1,0],[0,1,0,0,0,1,0],[2,0,1,1,1,0,2],[2,2,0,0,0,2,2]]
charset5[86]=[[2,0,2,2,2,0,2],[0,1,0,2,0,1,0],[0,1,0,2,0,1,0],[2,0,1,0,1,0,2],[2,0,1,0,1,0,2],[2,2,0,1,0,2,2],[2,2,2,0,2,2,2]]
charset5[87]=[[2,0,2,2,2,0,2],[0,1,0,2,0,1,0],[0,1,0,0,0,1,0],[0,1,0,1,0,1,0],[0,1,0,1,0,1,0],[2,0,1,0,1,0,2],[2,2,0,2,0,2,2]]
charset5[88]=[[2,0,2,2,2,0,2],[0,1,0,2,0,1,0],[2,0,1,0,1,0,2],[2,2,0,1,0,2,2],[2,0,1,0,1,0,2],[0,1,0,2,0,1,0],[2,0,2,2,2,0,2]]
charset5[89]=[[2,0,2,2,2,0,2],[0,1,0,2,0,1,0],[0,1,0,2,0,1,0],[2,0,1,0,1,0,2],[2,2,0,1,0,2,2],[2,2,0,1,0,2,2],[2,2,2,0,2,2,2]]
charset5[90]=[[2,0,0,0,0,0,2],[0,1,1,1,1,1,0],[2,0,0,0,1,0,2],[2,2,0,1,0,2,2],[2,0,1,0,0,0,2],[0,1,1,1,1,1,0],[2,0,0,0,0,0,2]]
charset5[91]=[[2,0,0,0,2],[0,1,1,1,0],[0,1,0,0,2],[0,1,0,2,2],[0,1,0,0,2],[0,1,1,1,0],[2,0,0,0,2]]
charset5[92]=[[2,0,2,2,2,2,2],[0,1,0,2,2,2,2],[2,0,1,0,2,2,2],[2,2,0,1,0,2,2],[2,2,2,0,1,0,2],[2,2,2,2,0,1,0],[2,2,2,2,2,0,2]]
charset5[93]=[[2,0,0,0,2],[0,1,1,1,0],[2,0,0,1,0],[2,2,0,1,0],[2,0,0,1,0],[0,1,1,1,0],[2,0,0,0,2]]
charset5[94]=[[2,2,2,0,2,2,2],[2,2,0,1,0,2,2],[2,0,1,0,1,0,2],[0,1,0,2,0,1,0],[2,0,2,2,2,0,2],[2,2,2,2,2,2,2],[2,2,2,2,2,2,2]]
charset5[95]=[[2,2,2,2,2,2,2],[2,2,2,2,2,2,2],[2,2,2,2,2,2,2],[2,2,2,2,2,2,2],[2,0,0,0,0,0,2],[0,1,1,1,1,1,0],[2,0,0,0,0,0,2]]

#########################
## AUXILLARY FUNCTIONS ##
#########################

def drawPolygon(B,p):
	for i in range(len(p)):
		x1=p[i][0]
		y1=p[i][1]
		if i==len(p)-1:
			x2=p[0][0]
			y2=p[0][1]
		else:
			x2=p[i+1][0]
			y2=p[i+1][1]
		drawLine(B,x1,y1,x2,y2)

def drawLine(B,x1,y1,x2,y2):
	dx=abs(x2-x1)
	dy=abs(y2-y1)
	if dx==0 and dy==0:
		B[x1][y1]=1
		return
	if dx>dy:
		if x2 > x1:
			for x in range(x1,x2+1):
				rampStep=(x-x1)/(x2-x1)
				y=round((y2-y1)*rampStep)+y1
				if checkDrawOutOfBounds(x,y):
					B[x][y]=1
		else:
			for x in range(x2, x1+1):
				rampStep=(x-x2)/(x1-x2)
				y=round((y1-y2)*rampStep)+y2
				if checkDrawOutOfBounds(x,y):
					B[x][y]=1
	else:
		if y2>y1:
			for y in range(y1,y2+1):
				rampStep=(y-y1)/(y2-y1)
				x=round((x2-x1)*rampStep)+x1
				if checkDrawOutOfBounds(x,y):
					B[x][y]=1
		else:
			for y in range(y2,y1+1):
				rampStep=(y-y2)/(y1-y2)
				x=round((x1-x2)*rampStep)+x2
				if checkDrawOutOfBounds(x,y):
					B[x][y]=1

def checkDrawOutOfBounds(x,y):
	return(x>=0)&(x<48)&(y>=0)&(y<12)

ditherMat=[0,4/8,1/8,5/8,6/8,2/8,7/8,3/8,3/16,11/16,1/16,9/16,15/16,7/16,13/16,5/16]
def dithering(B):
	for x in range(48):
		for y in range(12):
			B[x][y]=1 if B[x][y]>ditherMat[(x%4)*4+(y%4)]else 0

def clearBuffer(buffer):
	for x in range(48):
		for y in range(12):
			buffer[x][y]=0

#############
## EFFECTS ##
#############

class GenshikenLogo(kgfx.Effect):
	logo1=[
		[2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],
		[2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],
		[2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],
		[2,2,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,2,2,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,2,2,2,2],
		[2,2,0,0,1,1,1,0,0,1,1,0,0,1,1,1,0,0,0,1,1,1,0,1,0,0,0,0,1,0,1,0,1,0,0,0,1,1,0,0,1,1,1,0,0,2,2,2],
		[2,2,0,1,0,0,0,0,1,0,0,1,0,1,0,0,1,0,1,0,0,0,0,1,1,1,0,0,0,0,1,1,1,0,0,1,0,0,1,0,1,0,0,1,0,2,2,2],
		[2,2,0,1,0,0,1,0,1,1,1,1,0,1,0,0,1,0,0,0,0,1,0,1,0,0,1,0,1,0,1,0,0,1,0,1,1,1,1,0,1,0,0,1,0,2,2,2],
		[2,2,0,0,1,1,1,0,0,1,0,0,0,1,0,0,1,0,1,1,1,0,0,1,0,0,1,0,1,0,1,0,0,1,0,0,1,0,0,0,1,0,0,1,0,2,2,2],
		[2,2,2,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,2,2,2],
		[2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],
		[2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],
		[2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],
	]
	logo2=[
		[0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0],
		[0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,1,1,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0],
		[0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,1,1,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,0,0],
		[0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,1,1,0,0,0,0,1,0,1,0,0,0,0,0,0,0,1,1,0,0,0,1,1,1,1,1,0,0],
		[0,0,0,1,1,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,1,1,0,0,1,0,0,0,1,1,0,0,0,0,0,1,1,1,1,0,0,1,1,1,1,0,0,0],
		[0,0,1,1,1,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,1,0,0,1,0,0,0,1,0,0,0,0,1,1,1,1,1,0,0,0,0,0,1,1,0,0,0],
		[0,1,1,1,1,0,0,1,0,1,1,1,1,0,0,0,0,0,0,0,0,0,0,1,1,0,1,0,1,0,0,0,0,0,1,1,1,1,0,0,0,0,1,1,0,0,0,0],
		[0,1,1,1,1,0,0,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,1,1,1,1,0,1,0,0,0,0,0,0,1,1,1,0,0,0,0,1,1,1,0,0,0],
		[0,0,0,1,1,0,0,1,1,0,1,1,1,0,0,0,0,0,0,0,0,0,0,1,1,1,1,0,1,0,0,0,0,0,0,1,1,0,0,0,0,0,1,1,1,1,0,0],
		[0,0,0,1,0,0,0,1,1,0,1,1,1,0,0,0,0,0,0,0,0,0,0,1,1,1,1,0,1,0,0,0,0,0,0,1,1,0,0,0,0,1,1,1,1,1,0,0],
		[0,0,0,1,0,0,0,1,1,1,1,1,1,0,0,0,0,0,0,1,1,0,0,1,0,1,0,0,1,0,0,0,0,0,0,1,1,0,0,0,0,1,0,0,1,1,0,0],
		[0,0,0,1,0,0,0,1,0,1,0,1,1,0,0,0,0,0,1,1,1,1,0,1,0,1,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,1,0,1,1,1,0],
		[0,0,0,1,1,0,0,1,0,1,1,1,1,0,0,0,0,1,1,1,1,1,0,1,1,1,1,0,1,0,0,0,0,0,1,1,0,0,0,0,1,0,1,1,1,1,1,1],
		[0,0,1,1,1,0,0,1,1,1,1,1,1,0,0,0,0,1,1,0,1,0,0,1,1,1,0,0,1,0,0,0,0,0,1,0,0,0,0,0,1,1,1,1,1,1,1,1],
		[0,1,1,1,1,0,0,1,1,1,1,1,1,0,0,0,1,1,0,0,1,0,1,1,1,1,0,0,1,0,0,0,0,1,1,0,0,1,1,1,1,1,1,1,1,1,0,0],
		[1,1,1,1,1,0,0,1,1,1,1,1,1,0,0,0,0,0,0,1,1,1,1,1,1,0,1,1,1,0,0,0,0,1,1,0,1,1,1,1,1,1,1,0,1,1,0,0],
		[1,1,0,1,1,0,0,1,0,1,1,1,1,0,0,0,0,0,0,1,1,1,0,1,1,1,1,1,1,0,0,0,0,1,0,1,1,1,1,1,1,1,0,0,0,1,0,0],
		[1,1,0,1,1,1,0,1,1,0,1,1,1,0,0,0,0,0,1,1,1,1,0,1,1,1,1,1,1,0,0,0,1,1,0,1,0,1,1,1,1,1,0,0,1,1,0,0],
		[0,1,1,1,0,1,0,1,1,1,1,1,1,0,0,0,0,0,1,1,1,1,0,1,1,1,1,1,1,0,0,0,1,1,1,0,0,1,1,0,1,1,0,0,1,1,0,0],
		[0,1,1,1,1,1,0,1,1,1,1,1,1,0,0,0,0,0,1,1,1,0,0,1,1,1,1,0,0,0,0,0,1,1,0,0,0,1,1,0,1,0,0,0,1,1,0,0],
		[0,1,1,1,1,0,0,1,1,1,1,1,0,0,0,0,0,1,1,1,1,0,0,1,0,1,1,0,0,0,0,0,1,1,0,0,1,1,0,0,1,0,0,0,1,1,0,0],
		[0,0,1,1,1,0,0,1,0,1,0,0,0,0,0,0,0,1,0,1,1,0,0,0,1,1,1,0,0,0,1,1,0,1,0,0,1,1,0,0,1,0,0,0,1,1,0,0],
		[0,0,1,1,0,0,0,0,0,1,0,0,0,0,1,0,0,1,0,1,1,0,0,0,1,1,1,0,0,0,1,1,0,1,1,1,1,0,0,0,1,0,0,0,1,1,0,0],
		[0,1,1,1,0,0,0,0,1,0,0,0,0,0,1,0,1,0,1,1,1,0,0,0,1,1,1,0,0,0,1,0,0,1,1,0,1,0,0,0,1,0,0,0,1,1,0,0],
		[0,1,1,0,0,0,0,0,1,1,0,0,0,0,1,0,1,1,1,1,1,0,0,1,0,1,1,0,0,0,1,0,0,0,1,0,0,0,0,0,1,0,0,0,1,1,0,0],
		[1,1,1,0,0,0,0,1,1,1,0,0,0,0,1,0,1,1,1,1,1,0,0,1,0,1,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,0,0,0,1,1,0,0],
		[1,1,0,0,0,0,0,1,0,1,0,0,0,0,1,1,1,1,0,1,1,0,1,1,0,1,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0],
		[1,0,0,0,0,0,1,1,0,1,0,0,0,0,1,1,1,0,0,1,1,0,1,0,0,1,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0],
		[0,0,0,0,0,0,1,0,0,1,0,0,0,0,1,0,0,0,0,1,1,0,1,0,0,1,1,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0],
		[0,0,0,0,0,0,1,0,0,1,0,0,0,1,1,0,0,0,0,1,1,0,0,0,0,0,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0],
		[0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,0,0,0,0,0,1,0,0,0,0,0,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0],
		[0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
	]
	def __init__(self,tstart):
		super().__init__(tstart)
		self.parameters["scroll"] = 0
	def render(self,out,ins,t,t_global,t_frame):
		B=out.buffer
		for y in range(12):
			offset=int((len(self.logo2)+12)*self.parameters["scroll"])-12+y
			for x in range(48):
				B[x][y]=self.logo2[offset][x]if(offset>=0 and offset<32)else 0
				if self.logo1[y][x]<2:
					B[x][y]=self.logo1[y][x]

class BitmaskLogo(kgfx.Effect):
	bitmask=[
		[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,],
		[0,0,1,1,0,1,1,1,0,1,1,0,1,1,1,1,1,1,0,1,1,0,0,0,1,0,1,1,0,1,1,1,0,1,1,1,1,1,1,0,1,1,0,0,1,1,0,0,],
		[0,0,1,1,1,0,0,1,0,1,1,0,0,0,0,0,0,0,0,1,1,0,0,1,1,0,1,1,1,0,0,1,0,1,1,0,0,0,0,0,1,1,0,0,1,1,0,0,],
		[0,0,1,1,0,0,1,0,0,1,1,0,1,1,1,1,1,1,0,1,1,0,1,0,1,0,1,1,0,0,0,1,0,1,1,1,1,1,1,0,1,1,0,1,1,0,0,0,],
		[0,0,1,1,1,1,1,1,0,1,1,0,0,0,1,1,0,0,0,1,1,1,1,0,1,0,1,1,1,1,1,1,0,0,0,0,0,1,1,0,1,1,0,1,1,0,0,0,],
		[0,0,1,1,0,0,0,1,0,1,1,0,0,0,1,1,0,0,0,1,1,0,1,0,1,0,1,1,0,0,0,1,0,1,0,0,1,1,1,0,1,1,1,1,0,0,0,0,],
		[0,0,1,1,0,0,0,1,0,0,0,0,0,1,1,1,0,0,0,1,1,0,1,0,1,0,1,1,0,0,0,1,0,0,0,1,1,1,0,0,1,1,1,0,0,1,0,0,],
		[0,0,1,1,0,1,1,0,0,1,1,0,1,1,1,0,0,0,0,1,1,0,1,0,1,0,1,1,0,0,1,0,0,1,1,1,1,0,0,0,1,1,0,0,1,1,0,0,],
		[0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,],
		[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,],
		[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,],
		[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,],
	]
	bitmaskDrips={0.5:[3,8],0.75:[29,5],0.9:[41,8],1.2:[9,9],1.35:[36,8],1.5:[22,8],1.7:[14,8],1.95:[36,9],2.05:[3,9],2.3:[41,9],2.45:[26,8],2.7:[9,10],2.95:[22,9],3.05:[14,9],3.2:[3,10],3.45:[41,10],3.65:[9,11],3.9:[36,10]}
	keysBitmaskDrips=list(bitmaskDrips.keys())
	def __init__(self,tstart):
		super().__init__(tstart)
	def render(self,out,ins,t,t_global,t_frame):
		B=out.buffer
		for x in range(48):
			for y in range(12):
				B[x][y]=self.bitmask[y][x]
		for k in range(len(self.keysBitmaskDrips)):
			if t>self.keysBitmaskDrips[k]:
				B[self.bitmaskDrips[self.keysBitmaskDrips[k]][0]][self.bitmaskDrips[self.keysBitmaskDrips[k]][1]]=1
		littleDripY1=3+round(math.tan(t%(math.pi/2)))
		littleDripY2=7+round(math.tan((t+0.5)%(math.pi/2)))
		if littleDripY1<11:
			B[17][littleDripY1]=1
		if littleDripY2<11:
			B[30][littleDripY2]=1

class Rotozoomer(kgfx.Effect):
	def __init__(self, tstart):
		super().__init__(tstart)
		self.parameters["dizziness"] = 0
	def render(self,out,ins,t,t_global,t_frame):
		angle=t/1.5
		dizzyX=self.parameters["dizziness"]*48
		dizzyY=self.parameters["dizziness"]*12
		for x in range(48):
			for y in range(12):
				xOffset=x-24
				yOffset=y-6
				trigParam=math.atan2(yOffset+dizzyY,xOffset+dizzyX)+angle
				hypoParam=math.sqrt(yOffset**2+xOffset**2)
				mappedY=round((math.sin(trigParam)*hypoParam)*math.sin(t/5))
				mappedX=round((math.cos(trigParam)*hypoParam)*math.sin(t/5))
				out.buffer[x][y]=(mappedX%8<4)^(mappedY%8>=4)

class RegularPolygon(kgfx.Effect):
	def __init__(self,tstart):
		super().__init__(tstart)
		p=self.parameters
		p["sides"]=3
		p["size"]=1
		p["cx"]=24
		p["cy"]=6
		p["speed"]=2
	def render(self,out,ins,t,t_global,t_frame):
		p=self.parameters
		points=[]
		sides=round(p["sides"])
		size=abs(p["size"])*6
		cx=p["cx"]
		cy=p["cy"]
		speed=p["speed"]
		for i in range(sides):
			k=i*2*math.pi/sides
			x=int(math.cos(k+t*speed)*size)+cx
			y=int(math.sin(k+t*speed)*size)+cy
			points.append([int(x),int(y)])
		if len(ins)>0:
			for x in range(48):
				for y in range(12):
					inside=1
					for i in range(sides):
						v1=points[i]
						v2=points[(i+1)%sides]
						inside&=((x-v2[0])*(v1[1]-v2[1])-(v1[0]-v2[0])*(y-v2[1]))>0;
					if inside:
						out.buffer[x][y]=ins[0].buffer[x][y]
		drawPolygon(out.buffer, points)

class Scroller(kgfx.Effect):
	def __init__(self,tstart):
		super().__init__(tstart)
		self.options["text"]="x"
		self.parameters["speed"]=15
	def render(self,out,ins,t,t_global,t_frame):
		scrollerXOffset=48-int(t*self.parameters["speed"])
		for charascii in self.options["text"]:
			char=charset5[ord(charascii)]or charset5[ord(charascii.upper())]or charset5[32]
			if scrollerXOffset+len(char[0])>=0:
				scrollerYOffset=int(math.sin(scrollerXOffset/10-t)*2*(math.sin(t/2)**2+1)-0.5)+3
				for indexRow,row in enumerate(char):
					for indexPixel,pixel in enumerate(row):
						pixelX=scrollerXOffset+indexPixel
						pixelY=indexRow+scrollerYOffset
						if pixel<2 and checkDrawOutOfBounds(pixelX,pixelY):
							out.buffer[pixelX][pixelY]=pixel
			scrollerXOffset=scrollerXOffset+len(char[0])-1
			if scrollerXOffset>47:
				break

class Stains(kgfx.Effect):
	def __init__(self,tstart):
		super().__init__(tstart)
	def render(self,out,ins,t,t_global,t_frame):
		for x in range(48):
			for y in range(12):
				xOffset=x+math.sin(t*2)*20
				yOffset=y+math.cos(t*1.5)*25
				xElong=2.5+math.sin(t*4)
				yElong=2.5+math.cos(t*1.5)/2
				out.buffer[x][y]=max((0.5+(math.sin(xOffset/xElong)/2)+(math.sin(yOffset/yElong)/2))/1.5,0);
		dithering(out.buffer)

class Twister(kgfx.Effect):
	def __init__(self,tstart):
		super().__init__(tstart)
	def render(self,out,ins,t,t_global,t_frame):
		clearBuffer(out.buffer)
		for col in range(48):
			colsin=col*math.cos(t)
			param=math.sin(t)+(math.sin(t*2.5)*math.sin(t*1.5))+(math.sin((colsin/24))*(math.pow(colsin/10,2)/10))
			angle1=(t+param)%(2*math.pi)
			angle2=(angle1+math.pi/2)%(2*math.pi)
			angle3=(angle1+math.pi)%(2*math.pi)
			angle4=(angle1+math.pi*1.5)%(2*math.pi)
			angles=[angle1,angle2,angle3,angle4]
			sinList=[math.sin(angle1),math.sin(angle2),math.sin(angle3),math.sin(angle4)]
			cosList=[math.cos(angle1),math.cos(angle2),math.cos(angle3),math.cos(angle4)]
			indexLeftmostVertex=cosList.index(min(cosList))
			del angles[indexLeftmostVertex]
			del sinList[indexLeftmostVertex]
			del cosList[indexLeftmostVertex]
			indexRightmostVertex=cosList.index(max(cosList))
			rowRightmostVertex=math.floor(sinList[indexRightmostVertex]*6+6)
			out.buffer[col][rowRightmostVertex]=cosList[indexRightmostVertex]
			vertex1=0
			if indexRightmostVertex==0:
				vertex1=1
			rowVertex1=math.floor(sinList[vertex1]*6+6)
			if rowVertex1<rowRightmostVertex:
				for row in range(rowRightmostVertex-rowVertex1):
					pixelColor=(cosList[vertex1]+(cosList[indexRightmostVertex]-cosList[vertex1])*(row/(rowRightmostVertex-rowVertex1))+1)/2
					if checkDrawOutOfBounds(col,rowVertex1+row):
						out.buffer[col][rowVertex1+row]=max(pixelColor*1.1,0)**2
			elif rowVertex1>rowRightmostVertex:
				for row in range(rowVertex1-rowRightmostVertex):
					pixelColor=(cosList[vertex1]+(cosList[indexRightmostVertex]-cosList[vertex1])*(((rowVertex1-rowRightmostVertex)-row)/(rowRightmostVertex-rowVertex1))+1)/2
					if checkDrawOutOfBounds(col,rowRightmostVertex+row):
						out.buffer[col][rowRightmostVertex+row]=max(pixelColor*1.1,0)**2
			vertex2=1
			if indexRightmostVertex==1 or vertex1==1:
				vertex2=2
			rowVertex2=math.floor(sinList[vertex2]*6+6)
			if rowVertex2<rowRightmostVertex:
				for row in range(rowRightmostVertex-rowVertex2):
					pixelColor=(cosList[vertex2]+(cosList[indexRightmostVertex]-cosList[vertex2])*(row/(rowRightmostVertex-rowVertex2))+1)/2
					if checkDrawOutOfBounds(col,rowVertex2+row):
						out.buffer[col][rowVertex2+row]=max(pixelColor*1.1,0)**2
			elif rowVertex2>rowRightmostVertex:
				for row in range(rowVertex2-rowRightmostVertex):
					pixelColor=(cosList[vertex2]+(cosList[indexRightmostVertex]-cosList[vertex2])*(((rowVertex2-rowRightmostVertex)-row)/(rowRightmostVertex-rowVertex2))+1)/2
					if checkDrawOutOfBounds(col, rowRightmostVertex + row):
						out.buffer[col][rowRightmostVertex+row]=max(pixelColor*1.1,0)**2
		dithering(out.buffer)

class Metaballs(kgfx.Effect):
	def __init__(self,tstart):
		super().__init__(tstart)
		self.lastTime=None
		self.metaballs=[]
		numMetaballs=4
		random.seed(0x2022EE30)
		for ball in range(numMetaballs):
			self.metaballs.append({"x":random.uniform(0,48),"y":random.uniform(0,12),"r":random.uniform(4,10),"vx":random.choice([1,-1])*random.uniform(2,4),"vy":random.choice([1,-1])*random.uniform(1,2)})
	def render(self,out,ins,t,t_global,t_frame):
		sumThreshold=5
		deltaT=t
		if self.lastTime!=None:
			deltaT=t-self.lastTime
		self.lastTime=t
		ballSpeed=6*deltaT
		for c in self.metaballs:
			c["x"]+=c["vx"]*ballSpeed
			c["y"]+=c["vy"]*ballSpeed
			if c["x"]<0:
				c["vx"]=abs(c["vx"])
				c["x"]=min(0-c["x"],47)
			
			if c["x"]>47:
				c["vx"]=-abs(c["vx"])
				c["x"]=max(96-c["x"],0)
			
			if c["y"]<0:
				c["vy"]=abs(c["vy"])
				c["y"]=min(0-c["y"],11)
			
			if c["y"]>11:
				c["vy"]=-abs(c["vy"])
				c["y"]=max(24-c["y"],0)
		for x in range(48):
			for y in range(12):
				sum=0
				closestD2=math.inf;
				for c in self.metaballs:
					dx=x-c["x"]
					dy=y-c["y"]
					d2=max(dx*dx+dy*dy,0.00001)
					sum+=c["r"]**2/d2
				out.buffer[x][y]=1 if sum>sumThreshold else 0

class Greets(kgfx.Effect):
	def __init__(self,tstart):
		super().__init__(tstart)
		self.options["name"]="x"
	def render(self,out,ins,t,t_global,t_frame):
		width=0
		chars=[]
		for charascii in self.options["name"]:
			char=charset5[ord(charascii)]or charset5[ord(charascii.upper())]or charset5[32]
			width+=len(char[0])-1
			chars.append(char)
		greetXOffset=math.floor(24-(width/2)-0.5)
		greetYOffset=2
		for indexChar,char in enumerate(chars):
			if greetXOffset+len(char[0])>=0:
				for indexRow,row in enumerate(char):
					for indexPixel,pixel in enumerate(row):
						pixelX=indexPixel+greetXOffset
						pixelY=indexRow+greetYOffset
						if pixel<2 and checkDrawOutOfBounds(pixelX,pixelY):
							out.buffer[pixelX][pixelY]=pixel
			greetXOffset+=len(char[0])-1

class BadApple(kgfx.Effect):
	def __init__(self,tstart):
		super().__init__(tstart)
		fp="ba.bin"
		self.vfile=open(fp,"rb")
		self.filefps=30.15
		self.filenumf=math.floor(os.path.getsize(fp)/72)
		self.lastframe=-1
		self.vbuffer=[[0]*12 for x in range(48)]
	def render(self,out,ins,t,t_global,t_frame):
		wantframe=math.floor(t*self.filefps)
		if wantframe!=self.lastframe:
			if wantframe>=0 and wantframe<self.filenumf:
				self.vfile.seek(72*wantframe)
				ndat=self.vfile.read(72)
				bit=0
				for y in range(12):
					for x in range(48):
						out.buffer[x][y]=self.vbuffer[x][y]=(ndat[bit>>3]>>(7-(bit&7)))&1
						bit+=1
			else:
				for y in range(12):
					for x in range(48):
						out.buffer[x][y]=0
		else:
			for y in range(12):
				for x in range(48):
					out.buffer[x][y]=self.vbuffer[x][y]
	def cleanup(self):
		self.vfile.close()

#####################
## TRANSITIONS ETC ##
#####################

class ClearBuffer(kgfx.Effect):
	def __init__(self,tstart):
		super().__init__(tstart)
	def render(self,out,ins,t,t_global,t_frame):
		clearBuffer(out.buffer)

class Life(kgfx.Effect):
	def __init__(self,tstart):
		super().__init__(tstart)
	def render(self,out,ins,t,t_global,t_frame):
		B=out.buffer
		tempMatrix=[[0]*12 for col in range(48)]
		N=[-1,0,1]
		for x in range(48):
			for y in range(12):
				tempSum=0
				for i in N:
					for j in N:
						if(i!=0 or j!=0)and checkDrawOutOfBounds(x+i,y+j):
							tempSum+=B[x+i][y+j]
				if(B[x][y]==1 and tempSum==2)or tempSum==3:
					tempMatrix[x][y]=1
		for x in range(48):
			B[x][:]=tempMatrix[x][:]

class FadeScanlines(kgfx.Effect):
	def __init__(self,tstart):
		super().__init__(tstart)
		self.parameters["fraction"]=0
	def render(self,out,ins,t,t_global,t_frame):
		fraction=self.parameters["fraction"]
		fadefrom=ins[0].buffer
		fadeto=ins[1].buffer
		for x in range(48):
			for y in range(12):
				faded=fadefrom[x][y]
				if y%2==1:
					if x<fraction*48:
						faded=fadeto[x][y]
				else:
					if(47-x)<fraction*48:
						faded=fadeto[x][y]
				out.buffer[x][y]=faded

class FadeDither(kgfx.Effect):
	def __init__(self,tstart):
		super().__init__(tstart)
		self.parameters["fraction"]=0
	def render(self,out,ins,t,t_global,t_frame):
		fraction=self.parameters["fraction"]
		fadefrom=ins[0].buffer
		for x in range(48):
			for y in range(12):
				out.buffer[x][y]=fadefrom[x][y]*(1-fraction)
		dithering(out.buffer)

class Wipe(kgfx.Effect):
	def __init__(self,tstart):
		super().__init__(tstart)
		self.parameters["fraction"]=0
		self.options["line"]="true"
	def render(self,out,ins,t,t_global,t_frame):
		B=out.buffer
		showline=(self.options["line"].lower()=="true")
		splitcol=round((1-self.parameters["fraction"])*(49 if showline else 48))-(1 if showline else 0)
		wleft=ins[0].buffer
		wright=ins[1].buffer
		for x in range(48):
			for y in range(12):
				if x<splitcol:
					B[x][y]=wleft[x][y]
				elif x == splitcol and showline:
					B[x][y]=1
				else:
					B[x][y]=wright[x][y]

class DropDown(kgfx.Effect):
	def __init__(self,tstart):
		super().__init__(tstart)
		self.parameters["fraction"]=0
	def render(self,out,ins,t,t_global,t_frame):
		drop=-round((1-self.parameters["fraction"])*13)
		back=ins[0].buffer
		front=ins[1].buffer
		for x in range(48):
			for y in range(12):
				if y-drop>=0 and y-drop<12:
					out.buffer[x][y]=front[x][y-drop]
				elif y-drop==12:
					out.buffer[x][y]=1
				else:
					out.buffer[x][y]=back[x][y]
