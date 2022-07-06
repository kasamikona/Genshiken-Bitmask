KGFX 0.1
# Test story
at 0:0/125
playmus pomcrop.mp3
addeffect checker E_Checkerboard $size=5 $speed=1 $distx=10 $disty=8
addeffect mirror E_Mirror $speed=1 $dist=1
addeffect gsklogo E_Genshiken
addeffect gskwobble E_OverWobble $wobble=0
addlayer 0 48 12
addlayer 1 48 12
addlayer 2 43 6
draw 2 gsklogo
loop
	1 checker
	0 mirror 1
	0 gskwobble 2
loopend
output 0
anim 10 checker size 2 10 fast

at 8:0/125
set gskwobble $wobble=1
at 9:0/125 # delayed exit
stopmus
