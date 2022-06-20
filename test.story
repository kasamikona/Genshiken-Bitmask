# Test story
playmus pomcrop.mp3
clreffects
addeffect checker E_Checkerboard 5 1 10 8
addeffect mirror E_Mirror 1 1
addeffect gsklogo E_Genshiken
addeffect gskwobble E_OverWobble
clrlayers
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

at 8:0/125
stopmus
at 8:1/125 # delayed exit
