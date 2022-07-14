KGFX 0.1
# Bitmask
# (c) Genshiken 2022
# Released at Euskal Encounter 30 Wild Compo

addlayer out 48 12
output out
addeffect clear ClearBuffer

at 0
playmus bitmask.mp3 0 # 138.69 BPM 16 beats per pattern
addeffect greets Greets
addeffect life Life
set greets name="ACHIFAIFA"
draw out greets
loop
loopend

at +8/138.69
loop
	out life
loopend

at 30 # delayed exit
stopmus
