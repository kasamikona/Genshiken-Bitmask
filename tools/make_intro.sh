dest=$PWD
tools=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
cd tools/..
rm -rf displays/__pycache__
rm -rf effects/__pycache__
echo "a=/tmp/genshiken;b=\$a/intro.tar.gz;echo Unpacking to \$a;mkdir \$a;tail -n+2 \$0>\$b;tar xzvf \$b -C \$a;echo;cd \$a;trap ' ' INT;\${PYTHON:=\"python\"} bitmask.py \$1;echo Cleaning up \$a;cd ..;rm -rf \$a;exit" > $dest/intro.sh
tar cvf - displays effects ba.bin bitmask.nsf bitmask.py demo.story kgfx.py ledmask.py | gzip -9 - >> $dest/intro.sh
