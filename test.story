KGFX 0.1
# Bitmask
# (c) Genshiken 2022
# Released at Euskal Encounter 30 Wild Compo

addlayer out 48 12
addlayer temp 48 12
output out
addeffect clear ClearBuffer
addeffect fdither FadeDither

at 0
playmus bitmask.mp3 0 # 138.69 BPM
addeffect genshiken GenshikenLogo $bgspeed=0
loop
	out genshiken
	out fdither
loopend

at 1:0/138.69
anim 3/138.69 fdither fraction 0 1 smooth

at 2:0/138.69
set fdither $fraction=0

at 3:0/138.69
anim 3/138.69 fdither fraction 0 1 smooth

at 4:0/138.69
set fdither $fraction=0
anim 2:0/138.69 genshiken scroll 0 1

at 7:0/138.69
deleffect fdither
addeffect tscanline FadeScanlines
addeffect bitmask BitmaskLogo
anim 1:0/138.69 tscanline fraction 0 1 linear
loop
	temp genshiken
	out bitmask
	out tscanline temp out
loopend

at 8:0/138.69
deleffect genshiken
deleffect tscanline
loop
	out bitmask
loopend

at 16:0/138.69
deleffect bitmask
addeffect scroller Scroller text=\
"we're back at wild compo, euskal 30!  12h to first blit, \
many more to get here.  stg7: fx, art, code  ksk: music, code"
loop
	out scroller
loopend

at 90 # delayed exit
stopmus
