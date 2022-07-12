KGFX 0.1
# Test story
at 0:0/125
playmus bitmask.mp3 272/138.69
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
loopend
output 0
anim 10 checker size 2 10 fast

at 1:10
loop
loopend
deleffect badapple

at 1:30 # delayed exit
stopmus
