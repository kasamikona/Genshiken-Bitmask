KGFX 0.1
# Bitmask
# (c) Genshiken 2022
# Released at Euskal Encounter 30 Wild Compo

addlayer out 48 12
output out
addeffect clear ClearBuffer
addlayer nothing 48 12
draw nothing clear

at 0
playmus bitmask.nsf 0 # 138.69 BPM
addeffect genshiken GenshikenLogo $bgspeed=0
addeffect fdither FadeDither
loop
	out genshiken
	out fdither out
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
addeffect fscanline FadeScanlines
addeffect bitmask BitmaskLogo
anim 1:0/138.69 fscanline fraction 0 1 linear
addlayer logotemp 48 12
loop
	logotemp genshiken
	out bitmask
	out fscanline logotemp out
loopend

at 8:0/138.69
dellayer logotemp
deleffect genshiken
deleffect fscanline
loop
	out bitmask
loopend

at 12:0/138.69
addeffect poly RegularPolygon $sides=3 $speed=2
anim 1:0/138.69 poly size 0 7 slow
loop
	out bitmask
	out poly
loopend

at 13:0/138.69
addlayer polyclip 48 12
anim 1:0/138.69 poly size 7 0
loop
	polyclip bitmask
	out clear
	out poly polyclip
loopend

at 14:0/138.69
deleffect bitmask
dellayer polyclip
anim 2/138.69 poly size 0 1.3
loop
	out clear
	out poly
loopend

at 14:2/138.69
anim 2/138.69 poly size 1.3 1.1
addeffect polyl RegularPolygon $sides=3 $cx=8 $speed=-2
addeffect polyr RegularPolygon $sides=3 $cx=40 $speed=-2
anim 4/138.69 polyl size 0 1 fast
anim 4/138.69 polyr size 0 1 fast
loop
	out clear
	out poly
	out polyl
	out polyr
loopend

at 15:0/138.69
set polyl $sides=4
set polyr $sides=4

at 15:2/138.69
set polyl $sides=5

at 15:3/138.69
set polyl $sides=4
set polyr $sides=5
addeffect rotoz Rotozoomer

at 16:0/138.69
addlayer wipeto 48 12
addeffect wipe Wipe
loop
	out clear
	out poly
	out polyl
	out polyr
	wipeto rotoz
	out wipe out wipeto
loopend
anim 0:2/138.69 wipe fraction 0 1 fast

at 18:0/138.69
deleffect poly
deleffect polyl
deleffect polyr
deleffect wipe
dellayer wipeto
loop
	out rotoz
loopend
anim 2:0/138.69 rotoz dizziness 0 0.5 smooth

at 20:0/138.69
anim 2:0/138.69 rotoz dizziness 0.5 -0.5 smooth

at 22:0/138.69
anim 2:0/138.69 rotoz dizziness -0.5 0 smooth

at 25:0/138.69
addeffect meatballs Metaballs
addeffect dropdown DropDown
addlayer dropf 48 12
loop
	out rotoz
	dropf meatballs
	out dropdown out dropf
loopend
anim 2/138.69 dropdown fraction 0 1 slow

at 25:2/138.69
anim 1/138.69 dropdown fraction 1 0.6 fast
at 25:3/138.69
anim 1/138.69 dropdown fraction 0.6 1 slow

at 26:0/138.69
anim 1/138.69 dropdown fraction 1 0.8 fast
at 26:1/138.69
anim 1/138.69 dropdown fraction 0.8 1 slow

at 26:2/138.69
deleffect rotoz
deleffect dropdown
dellayer dropf
addeffect scroller Scroller $speed=21 text=\
"Hello Euskal!   Genshiken is back at wild compo   \
stg7: art, code, fx   ksk: code, fx, music   Greets to:"
loop
	out meatballs
	out scroller
loopend

at 42:0/138.69
draw out clear
deleffect meatballs
deleffect scroller
addeffect greets Greets
addeffect gol Life

set greets name="ACHIFAIFA"
loop
	out greets
loopend
at 42:2/138.69
loop
	out gol
loopend
at 43:0/138.69
set greets name="COLLAPSE"
loop
	out greets
loopend
at 43:2/138.69
loop
	out gol
loopend
at 44:0/138.69
set greets name="LFT"
loop
	out greets
loopend
at 44:2/138.69
loop
	out gol
loopend
at 45:0/138.69
set greets name="GARGAJ"
loop
	out greets
loopend
at 45:2/138.69
loop
	out gol
loopend
at 46:0/138.69
set greets name="IMOBILIS"
loop
	out greets
loopend
at 46:2/138.69
loop
	out gol
loopend
at 47:0/138.69
set greets name="MARCAN"
loop
	out greets
loopend
at 47:2/138.69
loop
	out gol
loopend
at 48:0/138.69
set greets name="SNS"
loop
	out greets
loopend
at 48:2/138.69
loop
	out gol
loopend
at 49:0/138.69
set greets name="SOGA"
loop
	out greets
loopend
at 49:2/138.69
loop
	out gol
loopend

at 50:0/138.69
deleffect greets
deleffect gol
addeffect stains Stains
loop
	out stains
loopend

at 57:0/138.69
addeffect twist Twister
addlayer wipeto 48 12
addeffect wipetwister Wipe
loop
	out stains
	wipeto twist
	out wipetwister out wipeto
loopend
anim 1:0/138.69 wipetwister fraction 0 1 smooth

at 65:0/138.69
dellayer wipeto
loop
	out twist
	out wipetwister out nothing
loopend
set wipetwister line=false
anim 1:0/138.69 wipetwister fraction 0 1 slow

at 66:0/138.69
deleffect stains
deleffect twist
deleffect wipetwister
addeffect badtext Greets
loop
	out clear
	out badtext
loopend
set badtext name="COULDN'T"
at 66:2/138.69
set badtext name="GIVE YOU"
at 67:0/138.69
set badtext name="A DEMO ON"
at 67:2/138.69
set badtext name="A SCREEN"
at 68:0/138.69
set badtext name="LIKE THIS"
addeffect apple BadApple
at 68:2/138.69
set badtext name="WITHOUT"
at 69:0/138.69
set badtext name="BADAPPLE"
at 69:1/138.69
addeffect tscanline FadeDither $fraction=1
addlayer bad 48 12
loop
	bad apple
	out clear
	out tscanline bad out
	out badtext
loopend
anim 0:3/138.69 tscanline fraction 1 0
at 69:2/138.69
set badtext name="RIGHT?"

at 70:0/138.69
deleffect badtext
deleffect tscanline
loop
	out apple
loopend

at 110:0/138.69
addeffect genshiken GenshikenLogo $bgspeed=0
addeffect poly RegularPolygon $sides=3 $speed=1.7
loop
	bad apple
	out genshiken
	out poly bad
loopend
anim 2:0/138.69 poly size 8 0 sharp

at 112:0/138.69
dellayer bad
deleffect apple
deleffect poly
addeffect fscanline FadeScanlines
loop
	out genshiken
	out fscanline out nothing
loopend

at 114:0/138.69
anim 1:2/138.69 fscanline fraction 0 1

at 116:0/138.69
deleffect fscanline
deleffect genshiken
loop
	out clear
loopend

at 117:0/138.69
stopmus
