KGFX 0.1
# Test story
at 0:0/125
playmus pomcrop.mp3
addeffect badapple BadApple
addeffect checker Checkerboard $size=5 $speed=1 $distx=10 $disty=8
addeffect mirror Mirror $speed=1 $dist=1
addeffect gsklogo Genshiken
addeffect gskwobble OverWobble $wobble=0
addlayer 0 48 12
addlayer 1 48 12
addlayer 2 43 6
draw 2 gsklogo
loop
	0 badapple
	0 gskwobble 2
loopend
output 0
anim 10 checker size 2 10 fast

at 8:0/125
set gskwobble $wobble=1
at 16:0/125 # delayed exit
stopmus
