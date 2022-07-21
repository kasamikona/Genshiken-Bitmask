dest=$PWD
tools=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
cd tools/..
rm -rf displays/__pycache__
rm -rf effects/__pycache__
echo "a=/tmp/genshiken;b=\$a/intro.tar.gz;echo Unpacking to \$a;mkdir \$a;tail -n+2 \$0>\$b;tar xzvf \$b -C \$a 2>/dev/null;echo;cd \$a;${PYTHON:=\"python\"} bitmask.py \$1;echo Cleaning up \$a;rm -rf \$a;exit" > $dest/intro.sh
tar cvf - displays effects ba.bin bitmask.nsf bitmask.py demo.story kgfx.py ledmask.py | gzip -9 - >> $dest/intro.sh
offset=$( stat --printf="%s" $dest/intro.sh )
echo "aaaa" >> $dest/intro.sh
echo "GENSHIKEN 2022" >> $dest/intro.sh
if [ ! -f $tools/forcecrc32.py ]; then
	curl -o $tools/forcecrc32.py https://www.nayuki.io/res/forcing-a-files-crc-to-any-value/forcecrc32.py
fi
python $tools/forcecrc32.py $dest/intro.sh $offset 600DC0DE
